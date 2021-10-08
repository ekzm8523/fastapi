from typing import Optional
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()
# app.include_router(router=)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







