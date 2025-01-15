from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from services.aws import SESService
from routes import tasks
from services import dynamodb
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)  # Get a logger instance

ses_service = SESService()
scheduler = AsyncIOScheduler()
@scheduler.scheduled_job('interval', seconds=10)
def periodic_task():
    print("Running periodic task")
    tasks = dynamodb.get_overdue_tasks()
    for task in tasks:
        logger.info('task {}'.format(task))
        logger.info(f"Task {task.task_name} is overdue!")
        # Send email
        if ses_service.send_task_email(task):
            # Update the notified field
            dynamodb.update_task(task.id, {"notified": True})

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: schedule and start tasks
    scheduler.start()
    yield
    # Shutdown: stop the scheduler
    scheduler.shutdown()

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