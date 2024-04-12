import secrets

import pytest


def test_wallet_is_created(user_api_request_context):
    user_id = secrets.token_hex(5)
    token = "ETH"
    response = user_api_request_context.post(url='/wallet/create', data={'userId': user_id, 'token': token})
    json_response = response.json()
    assert response.status == 201
    assert json_response['status'] == "success"
    assert json_response['data']['userId'] == user_id
    assert json_response['data'][token]
    assert json_response['data'][token] == str(0)
    assert json_response['data']['walletAddress']


@pytest.mark.parametrize("user_id, token, error_message", [
    (None, "ETH", "Missing userId"),
    ("", "ETH", "Missing userId"),
    ("TEST", "", "Missing token"),
    ("TEST", None, "Missing token"),
])
def test_wallet_is_not_created_without_required_fields(user_api_request_context, user_id, token, error_message):
    response = user_api_request_context.post(url='/wallet/create', data={'userId': user_id, 'token': token})
    json_response = response.json()
    assert response.status == 400
    assert json_response['status'] == "error"
    assert json_response['message'] == error_message
