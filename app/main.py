from fastapi import FastAPI
from router.authenticate import router as auth_router
# create instance from fastapi
app = FastAPI()


# register router
app.include_router(auth_router)