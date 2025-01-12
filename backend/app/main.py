from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import tasks
from services import dynamodb
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  # Get a logger instance

async def check_tasks_async():
    while True:
        logger.info("Checking condition (async)...")
        # Your condition checking logic here
        await asyncio.sleep(30 * 60)

async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up lifepsan...")
    task = asyncio.create_task(check_tasks_async())
    yield
    # Shutdown logic
    logger.info("Shutting down lifespan...")
    task.cancel() # Cancel the task to prevent lingering processes
    try:
        await task # wait for the task to finish cancelling.
    except asyncio.CancelledError:
        pass # Expected when task is cancelled

app = FastAPI(lifespan=lifespan)

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

@app.on_event("startup")
async def startup_event_async():
    asyncio.create_task(check_condition_async())