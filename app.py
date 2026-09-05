from functools import lru_cache
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect, url_for, session
from tensorflow.keras.models import load_model

from flask import Flask, render_template, request, flash, redirect, url_for, session
import mysql.connector

from config import Config
from src.data_preprocessing import load_data, preprocess
from src.predict import predict_from_features


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "credit_model.h5"
DATASET_PATH = BASE_DIR / "dataset" / "credit_data.csv"


app = Flask(__name__)
app.secret_key = "credit_scoring_secret"
app.config.from_object(Config)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Siddu@9505",      # Leave empty if you did not set a password
    database="credit_scoring"
)

cursor = db.cursor(dictionary=True)
@app.context_processor
def inject_globals():
    return {"app_name": "Credit Scoring Prediction"}


@lru_cache(maxsize=1)
def get_scaler():
    data = load_data(str(DATASET_PATH))
    _, _, scaler = preprocess(data)
    return scaler


@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    if MODEL_PATH.stat().st_size == 0:
        raise ValueError(
            f"Model file at {MODEL_PATH} is empty. Please provide the saved TensorFlow model artifact."
        )
    return load_model(str(MODEL_PATH))


def parse_features(form_data):
    return {
        "age": int(form_data["age"]),
        "income": int(form_data["income"]),
        "loan_amount": int(form_data["loan_amount"]),
        "credit_history": int(form_data["credit_history"]),
        "employment_years": int(form_data["employment_years"]),
        "debt_ratio": float(form_data["debt_ratio"]),
    }


@app.route("/")
def index():
    return render_template("index.html", page_title="Home")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:
         session["username"] = user["username"]
         session["email"] = user["email"]

         flash("Login Successful!", "success")
         return redirect(url_for("dashboard"))
        else:
            flash("Invalid Email or Password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))
        
        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        db.commit()
       
        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", page_title="Register")
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)

    # Total predictions
    cursor.execute(
        "SELECT COUNT(*) AS total FROM prediction_history WHERE username=%s",
        (session["username"],)
    )
    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS low
        FROM prediction_history
        WHERE username=%s
        AND prediction='Low Credit Risk'
        """,
        (session["username"],)
    )
    low = cursor.fetchone()["low"]

    cursor.execute(
        """
        SELECT COUNT(*) AS high
        FROM prediction_history
        WHERE username=%s
        AND prediction='High Credit Risk'
        """,
        (session["username"],)
    )
    high = cursor.fetchone()["high"]

    cursor.close()

    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        total=total,
        low=low,
        high=high
    )
@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "username" not in session:
      flash("Please login first.", "warning")
      return redirect(url_for("login"))
    if request.method == "POST":

        try:
            features = parse_features(request.form)
            print("Features:", features)

            model = get_model()
            scaler = get_scaler()

            prediction = predict_from_features(model, scaler, features)
            print("Prediction:", prediction)

            result_data = {
                "risk_label": prediction["risk_label"],
                "score": f'{prediction["score"] * 100:.2f}%',
                "message": "Credit risk assessment completed successfully.",
            }

            print("Saving to database...")

            cursor.execute("""
                INSERT INTO prediction_history
                (username, age, income, loan_amount,
                 credit_history, employment_years,
                 debt_ratio, prediction, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session.get("username", "Guest"),
                features["age"],
                features["income"],
                features["loan_amount"],
                features["credit_history"],
                features["employment_years"],
                features["debt_ratio"],
                prediction["risk_label"],
                float(prediction["score"])
            ))

            db.commit()
            print("Prediction saved successfully!")

        except Exception as exc:
            print("ERROR:", exc)

            result_data = {
                "risk_label": "Prediction Unavailable",
                "score": "N/A",
                "message": str(exc),
            }

        return render_template("result.html", page_title="Result", result=result_data)

    return render_template("predict.html", page_title="Predict")

@app.route("/result")
def result():

    result_data = {
        "risk_label": request.args.get("risk_label", "Low Credit Risk"),
        "score": request.args.get("score", "0%"),
        "message": request.args.get(
            "message",
            "Credit risk assessment completed successfully."
        ),
    }

    return render_template(
        "result.html",
        page_title="Result",
        result=result_data
    )
  


@app.route("/history")
def history():

    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT username, prediction, created_at
        FROM prediction_history
        WHERE username=%s
        ORDER BY created_at DESC
    """, (session["username"],))

    rows = cursor.fetchall()
    cursor.close()

    history = []

    for row in rows:
        history.append({
            "name": row["username"],
            "risk": row["prediction"],
            "date": row["created_at"].strftime("%Y-%m-%d %H:%M")
        })

    return render_template(
        "history.html",
        page_title="History",
        history=history
    )
    
@app.route("/about")
def about():
    return render_template("about.html", page_title="About")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
