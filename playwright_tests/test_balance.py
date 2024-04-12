import pytest


def test_balance_is_zero_for_newly_created_wallet(user_api_request_context, created_wallet):
    wallet_address = created_wallet["walletAddress"]
    token = "ETH"
    response = user_api_request_context.get(url='/balance',
                                            params={'address': wallet_address, 'token': token})
    json_response = response.json()
    assert response.status == 200
    assert json_response['status'] == "success"
    assert json_response['data']['address'] == wallet_address
    assert json_response['data']['token'] == token
    assert json_response['data']['balance'] == str(0)


def test_invalid_token_cannot_be_found(user_api_request_context, created_wallet):
    wallet_address = created_wallet["walletAddress"]
    token = "TEST"
    response = user_api_request_context.get(url='/balance', params={'address': wallet_address, 'token': token})
    json_response = response.json()
    assert response.status == 404
    assert json_response['status'] == "error"
    assert json_response['message'] == f"{token} token not found"


def test_invalid_address_cannot_be_found(user_api_request_context):
    token = "TEST"
    response = user_api_request_context.get(url='/balance', params={'address': "TEST", 'token': token})
    json_response = response.json()
    assert response.status == 404
    assert json_response['status'] == "error"
    assert json_response['message'] == f"{token} address not found"


@pytest.mark.parametrize("token, address, expected_message", [
    ("", "TEST", "Missing token"),
    ("TEST", "", "Missing address")
])
def test_balance_with_missing_required_fields(user_api_request_context,
                                              token, address, expected_message):
    response = user_api_request_context.get(url='/balance', params={'address': address, 'token': token})
    json_response = response.json()
    assert response.status == 400
    assert json_response['status'] == "error"
    assert json_response['message'] == expected_message
