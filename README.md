# Credit Score Prediction System

A web-based Credit Score Prediction System built with **Python, Flask, MySQL, TensorFlow/Keras, HTML, CSS, Bootstrap, and JavaScript**.

The application allows users to register, enter financial and credit-related information, receive a credit score prediction, and view their previous prediction history through a web dashboard.

## Features

- User registration and login
- Secure session-based authentication
- Credit score prediction using a trained machine learning model
- Financial and credit profile input
- Prediction result display
- Prediction history tracking
- User dashboard
- MySQL database integration
- Responsive web interface
- Model training and data preprocessing scripts
- Prediction accuracy information

## Technologies Used

### Backend
- Python
- Flask
- MySQL
- mysql-connector-python

### Machine Learning
- TensorFlow / Keras
- Scikit-learn
- Pandas
- NumPy

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Tools
- Git
- GitHub
- VS Code

## Project Structure

```text
credit-score-prediction-system/
│
├── dataset/
│   └── credit_data.csv
│
├── model/
│   └── credit_model.h5
│
├── result/
│   └── accuracy.txt
│
├── src/
│   ├── data_preprocessing.py
│   ├── predict.py
│   └── train_model.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── dashboard.html
│   ├── history.html
│   ├── index.html
│   ├── login.html
│   ├── predict.html
│   ├── register.html
│   └── result.html
│
├── app.py
├── config.py
├── main.py
├── train_model.py
├── requirements.txt
└── README.md

How It Works

The system follows this general workflow:

User registers and logs into the application.
User provides financial and credit-related information.
The application preprocesses the input data.
The trained TensorFlow/Keras model processes the input.
The system generates a credit score prediction.
The prediction result is displayed to the user.
Prediction details can be stored and viewed through prediction history.
Database

The application uses MySQL for storing application and prediction-related data.

Create a MySQL database named:

CREATE DATABASE credit_scoring;

Make sure MySQL is running before starting the Flask application.

Database Configuration

The application reads the database password from the DB_PASSWORD environment variable.

On Windows PowerShell:

$env:DB_PASSWORD="your_mysql_password"

Do not place your actual database password directly inside the source code.

Installation
1. Clone the repository
git clone https://github.com/msiddhardha77-bot/credit-score-prediction-system.git
cd credit-score-prediction-system
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Configure MySQL

Create the credit_scoring database and configure the MySQL password using the DB_PASSWORD environment variable.

6. Run the application
python app.py

Then open the local Flask address shown in the terminal.

Model Training

The project includes scripts for preprocessing the dataset and training the machine learning model.

The main training-related files are:

src/data_preprocessing.py
src/train_model.py
train_model.py

The trained model is stored in:

model/credit_model.h5
Dataset

The project contains a sample credit-related dataset:

dataset/credit_data.csv

The dataset is used for preprocessing and machine learning model development.

Results

Model-related results are stored in:

result/accuracy.txt

The project can be further improved by evaluating the model using additional metrics such as:

Accuracy
Precision
Recall
F1-score
Confusion Matrix
Security

Sensitive configuration values should be stored using environment variables instead of being hard-coded in the source code.

The repository ignores common local and sensitive files using .gitignore, including:

.venv/
__pycache__/
.idea/
.agents/
.env
Future Improvements
Improve model accuracy with additional datasets
Add more detailed credit-risk categories
Add graphical analytics to the dashboard
Add model evaluation visualizations
Improve validation and error handling
Deploy the application to a cloud platform
Add role-based administration
Improve security and production configuration
Purpose

This project was developed as a portfolio/academic project to demonstrate practical experience with:

Python development
Flask web application development
Machine learning
MySQL database integration
Frontend development
Git and GitHub
Author

Siddhardha M

GitHub:
https://github.com/msiddhardha77-bot


### Step 3 — Save the README

Press:

**`Ctrl + S`**

Don't run Git commands yet.

Once you've saved it, tell me **“saved”** and we'll check the changes before committing and pushing them.