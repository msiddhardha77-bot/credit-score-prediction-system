import numpy as np

def predict_from_features(model, scaler, features):
    data = np.array([[
        features["age"],
        features["income"],
        features["loan_amount"],
        features["credit_history"],
        features["employment_years"],
        features["debt_ratio"],
    ]])

    data = scaler.transform(data)
    prediction = model.predict(data, verbose=0)
    score = float(prediction[0][0])

    if score > 0.5:
        return {
            "risk_label": "High Credit Risk",
            "score": score,
        }

    return {
        "risk_label": "Low Credit Risk",
        "score": score,
    }

def predict_credit(model, scaler):

    print("\nEnter Applicant Details")

    age = int(input("Age: "))
    income = int(input("Income: "))
    loan = int(input("Loan Amount: "))
    history = int(input("Credit History (1 good / 0 bad): "))
    employment = int(input("Employment Years: "))
    debt = float(input("Debt Ratio: "))

    result = predict_from_features(
        model,
        scaler,
        {
            "age": age,
            "income": income,
            "loan_amount": loan,
            "credit_history": history,
            "employment_years": employment,
            "debt_ratio": debt,
        },
    )

    print(result["risk_label"])
