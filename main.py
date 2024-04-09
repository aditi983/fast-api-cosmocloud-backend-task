from fastapi import FastAPI
from routes import students 

app = FastAPI()

app.include_router(students.router, prefix="/api")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
