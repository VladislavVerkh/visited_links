from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config, tasks
from app.api.routes import visited_domains, visited_links
from app.api.routes.exceptions import custom_exception_handler
from app.api.routes.exceptions import common_exception_handler


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(Exception, common_exception_handler)
    app.add_exception_handler(ValueError, custom_exception_handler)

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(visited_domains.router, prefix="/api")
    app.include_router(visited_links.router, prefix="/api")

    return app


app = get_application()
