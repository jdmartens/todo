from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import tasks
from services import dynamodb

app = FastAPI()

app.include_router(tasks.router)

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