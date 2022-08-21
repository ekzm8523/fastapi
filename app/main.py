import uvicorn
from app.container import ApplicationContainer


container: ApplicationContainer = ApplicationContainer()


@container.app.on_event('startup')
async def startup_event():
    print("start up fastapi")
    from app.api.router import main_router
    container.app.include_router(main_router)
    await container.db.create_database()


@container.app.on_event('shutdown')
async def shutdown_event():
    print("delete database complete")
    await container.db.delete_database()


if __name__ == '__main__':
    uvicorn.run("main:container.app", host="0.0.0.0", port=3000, reload=True)
