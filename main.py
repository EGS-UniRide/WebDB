from fastapi import FastAPI
from src import routers
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values("/tmp/secrets/.env")

def create_app():
    app = FastAPI()

    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers.router, prefix="/v1")

    return app

app = create_app()  

@app.on_event("startup")
def startup_db_client():
    # print("ARRANCOU", flush=True)
    #app.mongodb_client = MongoClient('mongodb://mongodb:27017')
    #app.database = app.mongodb_client["notifs"]
    app.mongodb_client = MongoClient(config["DB_URI"], username=config["DB_USER"], password=config["DB_PASS"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}