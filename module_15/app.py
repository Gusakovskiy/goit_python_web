from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import AsyncElasticsearch

_INDEX_NAME = 'book_store_index'
es_client = AsyncElasticsearch(hosts=['localhost:9200'])
app = FastAPI()


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int] = None
    email: Optional[str] = None


class Author(AuthorBase):
    author_id: str


class Book(BaseModel):
    author_id: int
    title: str
    description: str


@app.post("/authors/", status_code=201, response_model=Author)
async def add_author(author: AuthorBase) -> Author:
    info = await es_client.info()
    print(info)
    print(f'Add author {author}')
    body = author.dict()
    es_res = await es_client.index(index=_INDEX_NAME, body=body)
    print("Result elastic search ", es_res)
    response = Author(author_id=es_res["_id"], **body)
    return response


@app.get("/authors/", status_code=200, response_model=Author)
async def get_author(author_id: str) -> Author:
    res = await es_client.get(index=_INDEX_NAME, id=author_id)
    source = res.get('_source')
    if source is None:
        raise HTTPException(status_code=404, detail="No such author")
    response = Author(author_id=res["_id"], **source)
    return response


@app.delete("/authors/", status_code=204)
async def delete_author(author_id: str):
    res = await es_client.get(index=_INDEX_NAME, id=author_id)
    source = res.get('_source')
    if source is None:
        raise HTTPException(status_code=404, detail="No such author")
    await es_client.delete(index=_INDEX_NAME, id=author_id)


@app.put("/authors/", status_code=200)
async def update_author(author_id: str, author: AuthorBase):
    res = await es_client.get(index=_INDEX_NAME, id=author_id)
    source = res.get('_source')
    if source is None:
        raise HTTPException(status_code=404, detail="No such author")
    res = await es_client.update(index=_INDEX_NAME, id=author_id, body=author.dict())
    response = Author(author_id=res["_id"], **source)
    return response


@app.on_event("startup")
async def app_startapp():
    exists = await es_client.indices.exists(index=_INDEX_NAME)
    if not exists:
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        result = await es_client.indices.create(index=_INDEX_NAME, ignore=400)
        print(result)


@app.on_event("shutdown")
async def app_shutdown():
    await es_client.close()
