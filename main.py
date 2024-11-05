from fastapi import FastAPI
from database import init_database
from routes import router as artist_router

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    conn, db = init_database()
    app.arango_connection = conn
    app.database = db
    print("Connected to the ArangoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    if hasattr(app, "arango_connection"):
        app.arango_connection.disconnect()

app.include_router(artist_router, tags=["artists"], prefix="/artist")