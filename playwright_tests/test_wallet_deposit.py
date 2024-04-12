import pytest


@pytest.mark.parametrize("amount", [
    "0.000001",
    "0.000002",
    "99.99999999",
    "100"
])
def test_deposit_with_lowest_and_highest_deposits(user_api_request_context, created_wallet, amount):
    token = "ETH"
    wallet_address = created_wallet["walletAddress"]
    response = user_api_request_context.post(url='/wallet/deposit',
                                             data={'walletAddress': wallet_address,
                                                   'amount': amount,
                                                   'token': token})
    json_response = response.json()
    assert response.status == 201
    assert json_response['status'] == "success"
    assert json_response['data']['walletAddress'] == wallet_address
    assert json_response['data']['amountDeposited'] == amount
    assert json_response['data']['newBalance'] == amount
    assert json_response['data']['token'] == token

    response = user_api_request_context.get(url='/balance',
                                            params={'address': wallet_address, 'token': token})
    json_response = response.json()
    assert response.status == 200
    assert json_response['data']['balance'] == amount


@pytest.mark.parametrize("amount, expected_message", [
    ("0.0000009999", "Deposit amount 0.0000009999 must be at least 1000000000000 wei"),
    ("100.00000001", "Deposit amount 100.00000001 exceeds maximum allowed limit of 100000000000000000000 wei"),
    ("not_valid_decimal", "not_valid_decimal amount cannot be converted to decimal")
])
def test_deposit_with_amount_limits(user_api_request_context, created_wallet,
                                    amount, expected_message):
    token = "ETH"
    wallet_address = created_wallet["walletAddress"]
    response = user_api_request_context.post(url='/wallet/deposit', data={'walletAddress': wallet_address,
                                                                          'amount': amount,
                                                                          'token': token})
    json_response = response.json()
    assert response.status == 400
    assert json_response['status'] == "error"
    assert json_response['message'] == expected_message

    response = user_api_request_context.get(url='/balance',
                                            params={'address': wallet_address, 'token': token})
    json_response = response.json()
    assert response.status == 200
    assert json_response['data']['balance'] == created_wallet[token]


@pytest.mark.parametrize("amount, token, wallet_address, expected_message", [
    (None, "TEST", "TEST", "Missing deposit amount"),
    ("", "TEST", "TEST", "Missing deposit amount"),
    ("TEST", None, "TEST", "Missing deposit token"),
    ("TEST", "", "TEST", "Missing deposit token"),
    ("TEST", "TEST", None, "Missing deposit wallet address"),
    ("TEST", "TEST", "", "Missing deposit wallet address")
])
def test_deposit_with_missing_required_fields(user_api_request_context,
                                              amount, token, wallet_address, expected_message):
    response = user_api_request_context.post(url='/wallet/deposit', data={'walletAddress': wallet_address,
                                                                          'amount': amount,
                                                                          'token': token})
    json_response = response.json()
    assert response.status == 400
    assert json_response['status'] == "error"
    assert json_response['message'] == expected_message
