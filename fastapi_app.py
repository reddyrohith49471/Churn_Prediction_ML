from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.core.inference_service import InferenceService

app = FastAPI(
    title="Customer Churn Prediction",
    description="Web-based customer churn prediction system",
    version="1.0.0",
)

templates = Jinja2Templates(directory="templates")

predictor = InferenceService()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prediction": None
        }
    )


@app.post("/predict", response_class=HTMLResponse)
def predict_churn(
    request: Request,

    gender: str = Form(...),
    SeniorCitizen: int = Form(...),
    Partner: str = Form(...),
    Dependents: str = Form(...),
    tenure: int = Form(...),
    PhoneService: str = Form(...),
    MultipleLines: str = Form(...),
    InternetService: str = Form(...),
    OnlineSecurity: Optional[str] = Form("No"),
    OnlineBackup: Optional[str] = Form("No"),
    DeviceProtection: Optional[str] = Form("No"),
    TechSupport: Optional[str] = Form("No"),
    StreamingTV: Optional[str] = Form("No"),
    StreamingMovies: Optional[str] = Form("No"),
    Contract: str = Form(...),
    PaperlessBilling: str = Form(...),
    PaymentMethod: str = Form(...),
    MonthlyCharges: float = Form(...),
    TotalCharges: float = Form(...)
):
    """
    Handle churn prediction from form input.
    """

    input_data = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    prediction = predictor.predict(input_data)

    result = (
        "⚠️ Customer is likely to churn"
        if prediction == 1
        else "✅ Customer is not likely to churn"
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "prediction": result
        }
    )


@app.get("/health")
def health():
    """
    Health check endpoint for deployment & monitoring.
    """
    return {"status": "ok"}
