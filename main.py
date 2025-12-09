from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

            return olx_scrapper(OLX_URL)
        case _: 
            return {"message": 'Brak takiego dostawcy!'}