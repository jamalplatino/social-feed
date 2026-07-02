from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from sqlalchemy import Select
from app.schemas import PostResponse
from app.db import Post, create_async_engine, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
# from app.imageKit import imageKit
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


BASE_URL = "http://127.0.0.1:8000"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# @app.post("/pages/post")
# def post_page():
#     pass

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feeds(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(Select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]
    posts_data = []

    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at
            }
        )
    return {"posts": posts_data}