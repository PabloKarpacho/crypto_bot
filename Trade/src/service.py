import os 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_core._pydantic_core import ValidationError
from pybit.unified_trading import HTTP
from src.model import OrderRequest, AmendOrderRequest, CancelOrderRequest, GetOpenOrderRequest, CancelAllOrderRequest
from src.logger import init_log

app = FastAPI()

_logger = init_log()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    _logger.error(exc, exc_info=True)
    return JSONResponse(
        status_code=422,
        content={'detail': exc.errors(), 'body': exc.body}
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    _logger.error(exc, exc_info=True)
    return await http_exception_handler(request, exc)

session = HTTP(
    testnet=False,
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
)

@app.get("/get_status")
def get_status():
    return "Trade service is running!"

@app.post("/place_order")
def place_order(request: OrderRequest):

    responce = session.place_order(**request.model_dump(exclude_none=True))

    return responce

@app.post("/amend_order")
def amend_order(request: AmendOrderRequest):

    responce = session.amend_order(**request.model_dump(exclude_none=True))

    return responce

@app.post("/cancel_order")
def cancel_order(request: CancelOrderRequest):

    responce = session.cancel_order(**request.model_dump(exclude_none=True))

    return responce

@app.post("/get_open_orders")
def get_open_orders(request: GetOpenOrderRequest):

    responce = session.get_open_orders(**request.model_dump(exclude_none=True))

    return responce

@app.post("/cancel_all_orders")
def cancel_all_orders(request: CancelAllOrderRequest):

    responce = session.cancel_all_orders(**request.model_dump(exclude_none=True))

    return responce


