from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import automatic_house_edit


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/start')
def action():
    automatic_house_edit.execute()


@app.get('/')
def get():
    return {'detail': 'hello python'}
