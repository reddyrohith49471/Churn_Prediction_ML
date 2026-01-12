import streamlit as st
from src.core.inference_service import InferenceService

st.set_page_config(page_title="Churn Predictor", layout="centered")

predictor = InferenceService()

st.title("📊 Customer Churn Prediction")

st.markdown("Enter customer details below:")


gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", [0, 1])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=1)
phone = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox(
    "Multiple Lines",
    ["Yes", "No", "No phone service"]
)
internet = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)
online_security = st.selectbox(
    "Online Security",
    ["Yes", "No", "No internet service"]
)
online_backup = st.selectbox(
    "Online Backup",
    ["Yes", "No", "No internet service"]
)
device_protection = st.selectbox(
    "Device Protection",
    ["Yes", "No", "No internet service"]
)
tech_support = st.selectbox(
    "Tech Support",
    ["Yes", "No", "No internet service"]
)
streaming_tv = st.selectbox(
    "Streaming TV",
    ["Yes", "No", "No internet service"]
)
streaming_movies = st.selectbox(
    "Streaming Movies",
    ["Yes", "No", "No internet service"]
)
contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)


monthly_charges = st.number_input(
    "Monthly Charges", min_value=0.0, max_value=500.0, value=50.0
)
total_charges = st.number_input(
    "Total Charges", min_value=0.0, max_value=10000.0, value=100.0
)

if st.button("Predict Churn"):
    input_data = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    prediction = predictor.predict(input_data)

    if prediction == 1:
        st.error("⚠️ Customer is likely to churn.")
    else:
        st.success("✅ Customer is not likely to churn.")
