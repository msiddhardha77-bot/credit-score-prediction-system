import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path):
    data = pd.read_csv(path)
    return data

def preprocess(data):
    X = data.drop("credit_risk", axis=1)
    y = data["credit_risk"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler