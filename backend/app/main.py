from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import tasks
from services import dynamodb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(tasks.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url="/tasks")

@app.get("/db_init")
async def db_init():
    table_name = "TodoTasks"
    if not dynamodb.table_exists(table_name):
        dynamodb.create_table(table_name)
        return {"message": f"Table {table_name} created successfully"}
    return {"message": f"Table {table_name} already exists"}