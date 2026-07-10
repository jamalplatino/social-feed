from pathlib import Path

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from requests import request
from sqlalchemy import Select
from var_dump import var_dump
from app.db import PostResponse, create_async_engine, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.schemas import PostCreate
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

BASE_URL = "http://127.0.0.1:8000"    # <-- your FastAPI server


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # """Accepts an image, uploads to ImageKit.io, returns the URL."""
    # try:
    #     # Read file
    #     image_data = await file.read()
    #     if not image_data:
    #         raise HTTPException(400, "File is empty")

    #     # Upload (try with explicit options)
    #     upload_response = imageKit.files.upload(
    #         file=image_data,
    #         file_name=file.filename,
    #         options={
    #             "use_unique_file_name": True,
    #             "folder": "/posts"
    #         }
    #     )
        
    #     # Return the URL
    #     return {"url": upload_response.url}
    
    # except Exception as e:
    #     # Print the full error for debugging
    #     print(f"Error: {e}")
    #     raise HTTPException(500, detail=f"Upload failed: {str(e)}")
    pass
    

@app.post("/upload")
async def upload_file(
    post: PostCreate,
    session: AsyncSession = Depends(get_async_session)
):    
    post = PostResponse(
        subject=post.subject,
        url=post.image_url,
        description=post.description,
        content=post.content
    )

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feeds(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(Select(PostResponse).order_by(PostResponse.created_at.desc()))
    posts = [row[0] for row in result.all()]
    posts_data = []

    for post in posts:
        # var_dump(post)
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "description": post.description,
                "subject": post.subject,
                "content": post.content,
                "created_at": post.created_at
            }
        )
    return {"posts": posts_data}