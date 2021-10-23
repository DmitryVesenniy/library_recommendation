import uvicorn
from fastapi import FastAPI

from global_state.state import init

from routers.recommendation import router as recommendation_route

init()

app = FastAPI()

app.include_router(recommendation_route)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
