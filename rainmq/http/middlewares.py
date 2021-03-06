from sanic import Sanic
from sanic.config import Config
from sanic.exceptions import NotFound
from sanic.response import HTTPResponse
from sanic.request import Request

from rainmq.data import MongoClient
from rainmq.http.broker import SingleQueueBroker


async def set_security_headers(
    request: Request,
    response: HTTPResponse
) -> HTTPResponse:
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        return response


async def no_contents_handler(
    request: Request, exception
) -> HTTPResponse:
    return HTTPResponse(body=None, status=204)


async def not_found_handler(
    request: Request, exception
) -> NotFound:
    raise NotFound


async def initialize(app: Sanic, loop):
    config: Config = app.config
    await SingleQueueBroker.initialize()
    await MongoClient.initialize(
        config['DATABASE_HOST'], config['DATABASE_NAME']
    )
