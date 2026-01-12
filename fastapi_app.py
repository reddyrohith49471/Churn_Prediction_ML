from typing import Optional
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from helper import ChurnService

app = FastAPI(
    title="Customer Churn Prediction",
    description="Web-based customer churn prediction system",
    version="1.0.0",
)

templates = Jinja2Templates(directory="templates")

churn_service = ChurnService()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "prediction": None}
    )


@app.post("/predict", response_class=HTMLResponse)
def predict_churn(
    request: Request,
    background_tasks: BackgroundTasks,

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

    prediction = churn_service.predict(input_data)
    churn_service.log_inference(input_data)

    background_tasks.add_task(churn_service.maybe_trigger_drift)

    result = (
        "⚠️ Customer is likely to churn"
        if prediction == 1
        else "✅ Customer is not likely to churn"
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "prediction": result}
    )


@app.get("/health")
def health():
    return {"status": "ok"}
