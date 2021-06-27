import fastapi


from fastapi import APIRouter


router = APIRouter()

router.get("/")
def root():
    return {"mess": "hell"}