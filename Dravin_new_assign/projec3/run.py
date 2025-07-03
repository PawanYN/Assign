from fastapi import FastAPI
from pypdf import PdfReader
from openai import OpenAI
from pydantic import BaseModel
import json, os, sys
from dotenv import load_dotenv


import argparse
import tqdm
import time
from pathlib import Path




app = FastAPI()

#-----------------------------------------reading pdf------------------------
try:
    reader = PdfReader('data/CV-AKHIL-v2.pdf')
    page = reader.pages[0]
    text = page.extract_text()
    
except Exception as e:
    print(f"Error loading PDF file: {e}")
#-------------------------------------------------------------------------------------


#-----------------------------------laoding API key from .env-------------------------
load_dotenv(".env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    sys.exit("OPENROUTER_API_KEY not found in .env")

print(API_KEY)
#--------------------------------------------------------------------------------


#----------------------------LLM call/AI assistant-------------------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

#---pydantic class for structure the json---
class CalendarEvent(BaseModel):
    name: str
    rollNo:str
    email: str
    phone: str
    skills:list[str]
    experience:list[str]
    education:list[str]
       
#---Model configration---
response= client.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "system", "content": (
                    "You are an expert résumé parser."
                    "Return a JSON object that looks like this responce_format"
                    "if data is not available for any attribute then put as null"
                    "in experience can have following attribute company,title,start,end and location"
                    "in education you can have following attribute as institution,degree,start,end and location"
                    "Do not output anything else.")
        },
        
        {"role": "user", "content": text },
    ],
    response_format=CalendarEvent,
)
#-----Output of LLM-----
headings_json = response.choices[0].message.content
try:
    headings = json.loads(headings_json)
    print("data is available")
    print(json.dumps(headings, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("Model returned invalid JSON\n", headings_json)
    

data=json.dumps(headings, indent=2, ensure_ascii=False)
data=json.loads(data)

#-------------------------------------------------------------------------------



#______________________________________________________________________________
#                               FASTAPI app
#______________________________________________________________________________


@app.get("/")
def read_root():
    return {"message":text}

print("I am here")

@app.get("/personal_details")
def personal_details():
    return {"name":data["name"],"roll NO:":data["rollNo"],"email":data["email"],"phone no":data["phone"]}

@app.get("/skills")
def skills():
    return data["skills"]

@app.get("/education")
def education():
    return data["education"]

@app.get("/experience")
def experience():
    return data["experience"]