from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schema.models import *
from utils.model import get_response_from_model

app = FastAPI()
router = APIRouter()

# Allow all origins in this example. You might want to restrict this based on your requirements.
origins = ["*"]

# Add CORS middleware to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post(path="/model", response_model=TextResponse, summary="Retrieve answer from the chat model")
def get_answer(request: TextRequest):
    response = get_response_from_model(request.text)
    return TextResponse(response=response)

app.include_router(router)