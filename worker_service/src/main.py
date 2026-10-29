import asyncio
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taskiq.receiver import Receiver

from src.api.router import router
from src.infrastructure.container import Container
from src.infrastructure.handlers.exceptions import exception_handlers
from src.infrastructure.lifetime import AppLifetime
from src.infrastructure.messaging.broker import broker
from src.infrastructure.messaging.tasks import process_task


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    app_lifetime = AppLifetime()
    await app_lifetime.startup()
    try:
        if broker.find_task(process_task.task_name) is None:
            raise RuntimeError(
                f"Task {process_task.task_name!r} is not registered"
            )
        await broker.startup()
        try:
            stop_event = asyncio.Event()
            receiver = Receiver(
                broker,
                max_async_tasks=100,
                run_startup=False,
            )
            async with asyncio.TaskGroup() as task_group:
                task_group.create_task(receiver.listen(stop_event))
                try:
                    yield
                finally:
                    stop_event.set()
        finally:
            await broker.shutdown()
    finally:
        await app_lifetime.shutdown()
        await fastapi_app.state.dishka_container.close()

def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/api/openapi.json",
        exception_handlers=exception_handlers
    )
    fastapi_app.include_router(router)
    container = make_async_container(Container())
    setup_dishka(container=container, app=fastapi_app)
    setup_taskiq_dishka(container=container, broker=broker)
    return fastapi_app

app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
