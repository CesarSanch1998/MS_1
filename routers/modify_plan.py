from fastapi import APIRouter
from fastapi import HTTPException
from schema.model_plan import first_structure_modify,first_structure_modify_all
#/////////////Scripts//////////////////////////////////////////
from scripts.modify_plan import modify_plan_client,modify_plan_all_client
import os
from dotenv import load_dotenv

load_dotenv()
modify_client = APIRouter()

@modify_client.post("/modify-plan")
def modify_client_plan(data: first_structure_modify):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    # response = "aceptado"
    response = modify_plan_client(data.data)
    return HTTPException(status_code=202, detail=response)

@modify_client.post("/modify-plan-all")
def modify_all_client_plan(data: first_structure_modify_all):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    # response = "aceptado"
    response = modify_plan_all_client(data.olt,data.data)
    return HTTPException(status_code=202, detail=response)
