"""
Binance Futures Testnet Client Wrapper

SECURITY:
- API credentials loaded only from environment variables.
- Uses Binance Futures Testnet only.
- Never hardcodes API keys.
"""

import os

from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import (
    BinanceAPIException,
    BinanceRequestException,
)

load_dotenv()


class BinanceClient:
    """
    Wrapper around python-binance Client configured
    for Binance Futures Testnet.
    """

    TESTNET_URL = "https://testnet.binancefuture.com/fapi"

    def __init__(self):
        """Initialize Binance Futures Testnet client."""

        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.test_mode = os.getenv("TEST_MODE", "true").lower()

        if not self.api_key:
            raise ValueError("API_KEY not found in .env")

        if not self.api_secret:
            raise ValueError("API_SECRET not found in .env")

        if self.test_mode != "true":
            raise ValueError(
                "TEST_MODE must be true. "
                "This application supports Binance Futures Testnet only."
            )

        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            requests_params={
                "timeout": 10
            }
        )

        self.client.FUTURES_URL = self.TESTNET_URL

    def get_client(self):
        """Return underlying Binance client."""
        return self.client

    def validate_connection(self):
        """Validate connection to Binance Futures Testnet."""

        try:

            account = self.client.futures_account()

            if not account:
                return (
                    False,
                    "Empty response received from Binance Futures API."
                )

            return (
                True,
                "Successfully connected to Binance Futures Testnet."
            )

        except BinanceAPIException as e:

            return (
                False,
                f"Binance API Error: {e.message}"
            )

        except BinanceRequestException as e:

            return (
                False,
                f"Network Error: {str(e)}"
            )

        except Exception as e:

            return (
                False,
                f"Unexpected Error: {str(e)}"
            )