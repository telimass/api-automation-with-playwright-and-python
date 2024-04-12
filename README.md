# API Automation with Playwright and Python

## Description

My mock API Service is a Flask-based API for managing wallets and performing transactions.

## Installation

- Clone the repository:
  ```bash
  git clone https://github.com/telimass/api-automation-with-playwright-and-python.git

- Install dependencies:
  ```bash
  pip install -r requirements.txt

## Usage

To use the API, follow the instructions below:

### Endpoints

* **GET /balance**: Retrieve the balance for a specific address and token.
* **POST /wallet/create**: Create a new wallet address for a user.
* **POST /wallet/deposit**: Deposit tokens into a wallet.

### Examples

- Retrieve balance:
  ```bash
  curl -X GET "http://localhost:5000/balance?address=0x123&token=ETH"

- Create wallet:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"userId": "user123", "token": "ETH"}' "http://localhost:5000/wallet/create"

- Deposit into wallet:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"walletAddress": "0x456", "amount": "1.0", "token": "ETH"}' "http://localhost:5000/wallet/deposit"

### Testing

Before running tests, make sure to start the API service by executing the following command:

  ```bash
  python .\api_service\api.py
  ```

To run tests, execute the following command in separate command line window:

  ```bash
  pytest