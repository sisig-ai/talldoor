from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi import FastAPI, Request
import weaviate

from datastore import PAGE, init_datastore, load_tldr_pages
from tldr import (
    download_tldr_pages,
    tldr_pages_downloaded,
    tldr_pages_unzipped,
    unzip_tldr_pages,
)


weaviate_client: ContextVar[weaviate.Client] = ContextVar("weaviate_client")


@asynccontextmanager
async def lifespan(server: FastAPI):
    print("Server starting")
    if not tldr_pages_downloaded():
        await download_tldr_pages()
    if not tldr_pages_unzipped():
        unzip_tldr_pages()
    if not weaviate_client.get(None):
        weaviate_client.set(weaviate.Client("http://0.0.0.0:8080"))
        print("Connected to Weaviate")
    init_datastore(weaviate_client.get())
    load_tldr_pages(weaviate_client.get(), should_reload=False)
    yield
    print("Server shutting down")


server = FastAPI(lifespan=lifespan)


@server.get("/")
async def root():
    return {"message": "Hello World"}


@server.post("/ask")
async def ask(request: Request):
    request_json = await request.json()
    question = request_json["question"]
    include_matched_content = request_json.get("include_matched_content", False)
    client: weaviate.Client = weaviate_client.get(
        weaviate.Client("http://0.0.0.0:8080")
    )
    response = (
        client.query.get(
            class_name=PAGE["class"], properties=["content", "command", "category"]
        )
        .with_near_text({"concepts": [question]})
        .with_limit(3)
        .with_generate(
            grouped_task=f"Using the information here, answer this question: {question}"
        )
        .do()
    )
    search_results = response["data"]["Get"][PAGE["class"]]
    matched_content = [
        {"content": result["content"], "command": result["command"]}
        for result in search_results
    ]
    answer = search_results[0]["_additional"]["generate"]["groupedResult"]
    print(answer)
    response = {"answer": answer}
    if include_matched_content:
        response["matched_content"] = matched_content
    return response
