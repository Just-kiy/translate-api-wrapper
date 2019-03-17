# noinspection PyPackageRequirements
import pytest

import json
import logging

import asyncio

logger = logging.getLogger(__name__)


class EchoServer(asyncio.Protocol):
    http_response_template = (
        'HTTP/1.1 200 OK\r\n'
        'Content-Type: application/json\r\n'
        'Content-Length: {length}\r\n'
        'Connection: close\r\n'
        '\r\n'
        '{content}'
    )

    def connection_made(self, transport):
        # noinspection PyAttributeOutsideInit
        self.transport = transport

        peer_name = self.transport.get_extra_info('peername')
        logger.debug(f'[SERVER] Got connection from {peer_name}')

    def data_received(self, data: bytes):
        content = json.dumps({'echo': data.decode()})
        response = self.http_response_template.format(
            content=content,
            length=len(content)
        )
        self.transport.write(bytes(response, encoding='utf-8'))

        self.transport.close()
        logger.debug('[SERVER] Closed the client connection')


@pytest.fixture(autouse=True)
def echo_server(event_loop, unused_tcp_port):
    server_coro = event_loop.create_server(
        EchoServer,
        host='127.0.0.1',
        port=unused_tcp_port
    )

    server = event_loop.run_until_complete(server_coro)
    yield server

    server.close()
    event_loop.run_until_complete(server.wait_closed())
