from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConflictError, RequestError
_INDEX_NAME = 'book_store_index'
es_client = AsyncElasticsearch(hosts=['localhost:9200'])
app = FastAPI()


class Location(BaseModel):
    city_name: str
    latitude: float
    longitude: float


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    location: Optional[Location] = None
    age: Optional[int] = None


class Author(AuthorBase):
    author_id: str


class ListAuthors(BaseModel):
    authors: List[Author]


class BookBase(BaseModel):
    author_id: str
    title: str
    description: str
    publisher_name: Optional[str] = None


class Book(BookBase):
    book_id: str


class ListBooks(BaseModel):
    books: List[Book]


async def _get_document(doc_id: str) -> dict:
    res = await es_client.get(index=_INDEX_NAME, id=doc_id, ignore=404)
    return res


async def _get_document_by_type(document_type: str):
    res = await es_client.search(
        index=_INDEX_NAME,
        query={"terms": {"_doc": [document_type]}},
    )
    return res


async def get_document_or_error(doc_id, detail, status_code=400, expected_type=None):
    doc = await _get_document(doc_id)
    source = doc.get('_source')
    if source is None:
        raise HTTPException(status_code=status_code, detail=detail)
    if expected_type is not None:
        if source["_doc"] not in expected_type:
            raise HTTPException(status_code=status_code, detail=detail)
    return doc


@app.post("/authors/", status_code=201, response_model=Author)
async def add_author(author: AuthorBase) -> Author:
    body = author.dict()
    body["_doc"] = "author"
    try:
        es_res = await es_client.index(index=_INDEX_NAME, document=body)
    except (ConflictError, RequestError) as e:
        raise HTTPException(status_code=400, detail=e.error)
    doc_id = es_res["_id"]
    doc = await _get_document(doc_id)
    response = Author(author_id=doc_id, **doc["_source"])
    return response


@app.get("/authors/{author_id}", status_code=200, response_model=Author)
async def get_author(author_id: str):
    res = await get_document_or_error(author_id, "No such author", 404)
    response = Author(author_id=res["_id"], **res['_source'])
    return response


@app.get("/authors/", status_code=200, response_model=ListAuthors)
async def get_authors():
    res = await _get_document_by_type("author")
    hits = res['hits']['hits']
    authors = [
        Author(
            author_id=hit['_id'],
            **hit['_source']
        )
        for hit in hits
    ]
    return ListAuthors(authors=authors)


@app.delete("/authors/{author_id}", status_code=204)
async def delete_author(author_id: str):
    await get_document_or_error(author_id, "No such author", 404, ["author"])
    await es_client.delete(index=_INDEX_NAME, id=author_id)
    # TODO delete all books for given author


@app.put("/authors/{author_id}", status_code=200, response_model=Author)
async def update_author(author_id: str, author: AuthorBase):
    _res = await get_document_or_error(author_id, "No such author", 404, ["author"])
    doc = author.dict()
    doc["_doc"] = "author"
    try:
        es_res = await es_client.index(index=_INDEX_NAME, id=author_id, document=doc)
    except (ConflictError, RequestError) as e:
        raise HTTPException(status_code=400, detail=e.error)
    author_id = es_res["_id"]
    res = await get_document_or_error(author_id, "No such author", 404)
    response = Author(author_id=author_id, **res["_source"])
    return response


@app.post("/books/", status_code=201, response_model=Book)
async def add_book(book: BookBase) -> Book:
    await get_document_or_error(book.author_id, "No such author", 422, ["author"])
    body = book.dict()
    body["_doc"] = "book"
    try:
        es_res = await es_client.index(index=_INDEX_NAME, document=body)
    except (ConflictError, RequestError) as e:
        raise HTTPException(status_code=400, detail=e.error)
    print("Book added", es_res)
    doc_id = es_res["_id"]
    doc = await _get_document(doc_id)
    response = Book(book_id=doc_id, **doc["_source"])
    return response


@app.get("/books/{book_id}", status_code=200, response_model=Book)
async def get_book(book_id: str) -> Book:
    res = await get_document_or_error(book_id, "No such book", 404, ["book"])
    response = Book(book_id=res["_id"], **res["_source"])
    return response


@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str):
    await get_document_or_error(book_id, "No such book", 404, ["book"])
    await es_client.delete(index=_INDEX_NAME, id=book_id)


@app.put("/books/{book_id}", status_code=200, response_model=Book)
async def update_book(book_id: str, book: BookBase) -> Book:
    await get_document_or_error(book_id, "No such book", 404, ["book"])
    await get_document_or_error(book.author_id, "No such author", 422, ["author"])
    doc = book.dict()
    doc["_doc"] = "book"
    try:
        res = await es_client.index(
            index=_INDEX_NAME,
            id=book_id,
            document=doc,
        )
    except (ConflictError, RequestError) as e:
        raise HTTPException(status_code=400, detail=e.error)
    response = Book(author_id=res["_id"], **res["_source"])
    return response


@app.get("/books/", status_code=200, response_model=ListBooks)
async def get_books():
    res = await _get_document_by_type("book")
    hits = res["hits"]["hits"]
    books = [
        Book(
            book_id=hit['_id'],
            **hit['_source']
        )
        for hit in hits
    ]
    return ListBooks(books=books)


@app.on_event("startup")
async def app_startapp():
    info = await es_client.info()
    print('')
    print('ELASTIC search info', info)
    print('')
    exists = await es_client.indices.exists(index=_INDEX_NAME)
    if not exists:
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        result = await es_client.indices.create(index=_INDEX_NAME, ignore=400)
        print(result)


@app.on_event("shutdown")
async def app_shutdown():
    await es_client.close()
