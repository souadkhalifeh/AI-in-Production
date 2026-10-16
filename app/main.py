from app.services.model_service import predict, load_model
from app.utils.logger import get_logger
# # Load the model when the script starts
# logger = get_logger()
# model = load_model()
from fastapi import FastAPI, Header, Depends
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.api.v1.prediction import router as prediction_router
from app.api.v1.users import router as users_router
from app.api.v1.feedback import router as feedback_router

def get_model_version():
    return "1.0.0"  # You can replace this with actual version retrieval logic
  
app = FastAPI(title="Iris Flower Prediction API", 
              version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to the Iris Flower Prediction API!"}

@app.get("/health")
def health():
    return{
        "status":"ready"
    }
# POST /api/v1/predict
app.include_router(prediction_router, 
                   prefix="/api/v1",
                   tags=["Predictions"])

@app.get("/predictions/{prediction_id}")
def get_prediction(prediction_id: int):
    return{
        "prediction": prediction_id,
    }

@app.get("/predictions/")
def get_prediction(limits: int =10):
    return{
        "limit": limits,
    }

@app.get("/header-demo")
def header_demo(user:str | None=Header(default=None)):
    return{
        "user": user
    }

@app.get("/version")
def version(model_version: str = Depends(get_model_version)):
    return {
        "model_version": model_version
    }


@app.get("/sync")
def sync_example():
    return {"message": "sync"}


@app.get("/async")
async def async_example():
    return {"message": "async"}


app.include_router(users_router, 
                   prefix="/api/v1", 
                   tags=["Users"])


app.include_router(
    feedback_router,
    prefix="/api/v1",
    tags=["Feedback"]
)