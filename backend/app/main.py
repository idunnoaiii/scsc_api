import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.db.base import User

app = FastAPI(title="SCSC API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def root():
    return "hello world"

# @app.get("/user")
# def get_user()
#     return 


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)