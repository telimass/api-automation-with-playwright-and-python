import secrets
from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext


@pytest.fixture(scope="session")
def user_api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="http://127.0.0.1:5000"
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="function")
def created_wallet(user_api_request_context: APIRequestContext):
    data = {"userId": secrets.token_hex(5), "token": "ETH"}
    response = user_api_request_context.post('/wallet/create', data=data)
    assert response.status == 201
    wallet_data = response.json()['data']
    yield wallet_data
