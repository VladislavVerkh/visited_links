from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST


async def common_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        {"status": f"error [{str(exc)}]"}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )


async def custom_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        {"status": f"error [{str(exc)}]"}, status_code=HTTP_400_BAD_REQUEST
    )
