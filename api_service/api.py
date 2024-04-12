import secrets
from decimal import Decimal, InvalidOperation

from flask import Flask, jsonify, request

app = Flask(__name__)

wallets = {}


def is_decimal(value):
    """
    Check if the provided value can be converted to a Decimal.
    """
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


def from_wei(wei_amount):
    """
    Takes a number of wei and converts it to ETH.
    """
    result_value = Decimal(wei_amount) / Decimal(10 ** 18)
    return Decimal(result_value)


def to_wei(eth_amount):
    """
    Takes a number of ETH and converts it to wei.
    """
    result_value = eth_amount * Decimal(10 ** 18)
    return int(result_value)


@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Retrieve the balance for a specific address and token.

    Returns:
        A JSON response containing the address, token, and balance if successful.
        If the token, or address is missing, returns a JSON response with an error message and status code 400.
        If the address or token is not found, returns a JSON response with an error message and status code 404.
    """
    address = request.args.get('address')
    token = request.args.get('token')

    if not address:
        return jsonify({"status": "error", "message": "Missing address"}), 400

    if not token:
        return jsonify({"status": "error", "message": "Missing token"}), 400

    if address not in wallets:
        return jsonify({"status": "error", "message": f"{address} address not found"}), 404

    if token not in wallets[address]:
        return jsonify({"status": "error", "message": f"{token} token not found"}), 404

    balance_eth = from_wei(wallets[address][token])
    return jsonify({
        "status": "success",
        "data": {
            "address": address,
            "token": token,
            "balance": str(balance_eth)
        }
    }), 200


@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    """
    Create a new wallet address for a user.

    Returns:
        A JSON response containing the new wallet address and associated user ID and token.
        If the user ID is missing, returns a JSON response with an error message and status code 400.
    """
    data = request.json
    user_id = data.get('userId')
    token = data.get('token')

    if not user_id:
        return jsonify({"status": "error", "message": "Missing userId"}), 400

    if not token:
        return jsonify({"status": "error", "message": "Missing token"}), 400

    def generate_wallet_address():
        return "0x" + secrets.token_hex(5)

    wallet_address = generate_wallet_address()
    wallets[wallet_address] = {
        "user_id": user_id,
        token: 0
    }
    return jsonify({
        "status": "success",
        "data": {
            "userId": user_id,
            "walletAddress": wallet_address,
            token: str(0)
        }
    }), 201


@app.route('/wallet/deposit', methods=['POST'])
def deposit_into_wallet():
    """
    Deposit tokens into a wallet.

    Returns:
        A JSON response indicating the success of the deposit and the updated balance.
        If the deposit amount, token, or wallet address is missing, returns a JSON response with an error message
        and status code 400. If the deposit amount is outside the allowed range, returns a JSON response with an
        error message and status code 400. If the wallet address or token is not found, returns a JSON response
        with an error message and status code 404.
    """

    data = request.json
    wallet_address = data.get('walletAddress')
    amount = data.get('amount')
    token = data.get('token')

    if not amount:
        return jsonify({"status": "error", "message": "Missing deposit amount"}), 400

    if not token:
        return jsonify({"status": "error", "message": "Missing deposit token"}), 400

    if not wallet_address:
        return jsonify({"status": "error", "message": "Missing deposit wallet address"}), 400

    if wallet_address not in wallets:
        return jsonify({"status": "error", "message": f"{wallet_address} address not found"}), 404

    if token not in wallets[wallet_address]:
        return jsonify({"status": "error", "message": f"{token} token not found"}), 404

    if not is_decimal(amount):
        return jsonify({"status": "error", "message": f"{amount} amount cannot be converted to decimal"}), 400

    amount_eth = Decimal(amount)
    amount_wei = to_wei(amount_eth)

    min_deposit = 1000000000000  # Example: minimum deposit amount
    max_deposit = 100000000000000000000  # Example: maximum deposit amount

    if amount_wei < min_deposit:
        return jsonify({"status": "error",
                        "message": f"Deposit amount {amount} must be at least {min_deposit} wei"}), 400
    elif amount_wei > max_deposit:
        return (jsonify({"status": "error",
                         "message": f"Deposit amount {amount} exceeds maximum allowed limit of {max_deposit} wei"}),
                400)

    wallets[wallet_address][token] += amount_wei
    new_balance_eth = from_wei(wallets[wallet_address][token])
    return jsonify({
        "status": "success",
        "data": {
            "walletAddress": wallet_address,
            "amountDeposited": str(amount_eth),
            "newBalance": str(new_balance_eth),
            "token": token
        }
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
