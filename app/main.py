from fastapi import FastAPI
from router.authenticate import router as auth_router
from router.posts import router as post_router
from router.comments import router as comment_router
# create instance from fastapi
app = FastAPI()


# register router
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)