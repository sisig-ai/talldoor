# talldoor

Answer questions using tldr man pages. Powered by Weaviate and FastAPI.

## Quick Start

1. Start Weaviate with `OPENAI_APIKEY="<your api key>" docker compose up -d`
2. Install dependencies with `pipenv install`
3. Run the server with `pipenv run python main.py` (this step will take long the first time, since the tldr pages need to fetched and loaded into Weaviate)
4. Ask a question with `http POST http://localhost:8000/ask question="how do i sort ls results by size?"`
