#this is for fast api 
from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import time, sys

app = FastAPI(titile="AI Fitness Coach")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
@app.get("/health")
def health_check():
    return{ "message":status.HTTP_200_OK ,"content ":"reaady to work " }
    