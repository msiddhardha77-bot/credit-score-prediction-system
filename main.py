from src.data_preprocessing import load_data, preprocess
from src.train_model import train_model
from src.predict import predict_credit

print("Credit Scoring Prediction System")

data = load_data("dataset/credit_data.csv")

X, y, scaler = preprocess(data)

model, accuracy = train_model(X, y)

print("Model Accuracy:", accuracy)



while True:

    print("\n1 Predict Credit Risk")
    print("2 Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        predict_credit(model, scaler)

    else:
        break


        