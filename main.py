from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from bs4 import BeautifulSoup

from scrappers import olx_scrapper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://bs-scrapper-fe.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"message": "API is running!"}

@app.get('/scrapper')
def get_data(provider: str, type: str, city: str):

    match provider:
        case 'olx':
            OLX_URL = f"https://www.olx.pl/praca/{city}/?search%5Bdist%5D=15"

            searchParamsURL = ""
            if (type == "student_status"):
                searchParamsURL = "&search%5Bfilter_enum_special_requirements%5D%5B0%5D=student_status";
            

            if (type == "remote_work_possibility"):
                searchParamsURL = "&search%5Bfilter_enum_workplace%5D%5B0%5D=remote_work_possibility";
            

            otherJobTypes = ["fulltime", "parttime", "halftime", "seasonal"];

            if (type in otherJobTypes):
                searchParamsURL = f"&search%5Bfilter_enum_type%5D%5B0%5D={type}";
            

            OLX_URL += searchParamsURL;
            resp = requests.get(OLX_URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, 'html.parser')
            print(OLX_URL)
            return olx_scrapper(soup)
        case _: 
            return {"message": 'Brak takiego dostawcy!'}