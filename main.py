from fastapi import FastAPI

from routers.posts.api.v1 import post_router
from routers.users.api.v1 import user_router

app = FastAPI()


app.include_router(user_router.router)
app.include_router(post_router.router)
