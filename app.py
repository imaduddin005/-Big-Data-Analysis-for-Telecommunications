import joblib
import numpy as np
from flask import Flask, request

# Load the trained model
model = joblib.load("random_forest_churn_model(9).joblib")

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Churn Prediction</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            margin: 40px; 
            background-color: #121212; /* Dark background */
            color: white; 
        }
        header {
            font-size: 24px;
            font-weight: bold;
            padding: 20px;
            background-color: #1e1e1e;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        form { 
            display: inline-block; 
            text-align: left; 
            background-color: #1e1e1e; 
            padding: 20px; 
            border-radius: 8px;
        }
        label { display: block; margin: 10px 0 5px; }
        input, select { 
            width: 100%; 
            padding: 8px; 
            background-color: #333; 
            color: white; 
            border: 1px solid #555; 
        }
        button { 
            margin-top: 15px; 
            padding: 10px 20px; 
            background-color: #007BFF; 
            color: white; 
            border: none; 
            cursor: pointer; 
        }
        button:hover {
            background-color: #0056b3;
        }
        h3 {
            margin-top: 20px;
            color: #ffcc00;
        }
    </style>
</head>
<body>
    <header>Customer Churn Prediction System</header>
    <h2>Predict if a Customer Will Churn</h2>
    <form method="post">
        <label>Gender (0=Female, 1=Male):</label>
        <input type="number" name="Gender" required>

        <label>Senior Citizen (0=No, 1=Yes):</label>
        <input type="number" name="SeniorCitizen" required>

        <label>Partner (0=No, 1=Yes):</label>
        <input type="number" name="Partner" required>

        <label>Dependents (0=No, 1=Yes):</label>
        <input type="number" name="Dependents" required>

        <label>Tenure (months):</label>
        <input type="number" name="Tenure" required>

        <label>Phone Service (0=No, 1=Yes):</label>
        <input type="number" name="PhoneService" required>

        <label>Multiple Lines (0=No, 1=Yes):</label>
        <input type="number" name="MultipleLines" required>

        <label>Internet Service (0=No, 1=DSL, 2=Fiber Optic):</label>
        <input type="number" name="InternetService" required>

        <label>Online Security (0=No, 1=Yes):</label>
        <input type="number" name="OnlineSecurity" required>

        <label>Online Backup (0=No, 1=Yes):</label>
        <input type="number" name="OnlineBackup" required>

        <label>Device Protection (0=No, 1=Yes):</label>
        <input type="number" name="DeviceProtection" required>

        <label>Tech Support (0=No, 1=Yes):</label>
        <input type="number" name="TechSupport" required>

        <label>Streaming TV (0=No, 1=Yes):</label>
        <input type="number" name="StreamingTV" required>

        <label>Streaming Movies (0=No, 1=Yes):</label>
        <input type="number" name="StreamingMovies" required>

        <label>Contract Type (0=Month-to-Month, 1=One year, 2=Two year):</label>
        <input type="number" name="ContractType" required>

        <label>Paperless Billing (0=No, 1=Yes):</label>
        <input type="number" name="PaperlessBilling" required>

        <label>Payment Method (0=Electronic, 1=Mailed Check, 2=Bank Transfer, 3=Credit Card):</label>
        <input type="number" name="PaymentMethod" required>

        <label>Monthly Charges:</label>
        <input type="text" name="MonthlyCharges" required>

        <label>Total Charges:</label>
        <input type="text" name="TotalCharges" required>

        <button type="submit">Predict Churn</button>
    </form>

    <h3>{result}</h3>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Get form data
            data = [
                int(request.form["Gender"]),
                int(request.form["SeniorCitizen"]),
                int(request.form["Partner"]),
                int(request.form["Dependents"]),
                int(request.form["Tenure"]),
                int(request.form["PhoneService"]),
                int(request.form["MultipleLines"]),
                int(request.form["InternetService"]),
                int(request.form["OnlineSecurity"]),
                int(request.form["OnlineBackup"]),
                int(request.form["DeviceProtection"]),
                int(request.form["TechSupport"]),
                int(request.form["StreamingTV"]),
                int(request.form["StreamingMovies"]),
                int(request.form["ContractType"]),
                int(request.form["PaperlessBilling"]),
                int(request.form["PaymentMethod"]),
                float(request.form["MonthlyCharges"]),
                float(request.form["TotalCharges"]),
            ]

            # Convert to numpy array & reshape
            sample_data = np.array([data])

            # Get prediction
            prediction = model.predict(sample_data)[0]
            result = f"Churn Prediction: <strong>{'Yes' if prediction == 1 else 'No'}</strong>"

            return HTML_FORM.replace("{result}", result)

        except Exception as e:
            return HTML_FORM.replace("{result}", f'<span style="color:red;">Error: {str(e)}</span>')

    return HTML_FORM.replace("{result}", "")

if __name__ == "__main__":
    app.run(debug=True)
