"""Simple CLI for trading_bot with improved error handling."""
import argparse
import os
import sys
from dotenv import load_dotenv

from bot.client import get_client
from bot.orders import place_order
from bot.validators import validate_order
from bot.logging_config import setup_logger


def print_api_key_status():
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    print("\nEnv check:")
    print(f"- API_KEY present: {bool(api_key)}")
    print(f"- API_SECRET present: {bool(api_secret)}")


def handle_binance_error(e: Exception):
    err = str(e)
    print("\nError communicating with Binance API:")
    print(f"- Raw: {err}\n")

    if "-2015" in err or "Invalid API-key" in err or "Invalid API-key, IP, or permissions for action" in err:
        print("Possible causes and fixes:")
        print("- Check the `trading_bot/.env` file contains `API_KEY` and `API_SECRET` and they are correct.")
        print("- If you configured IP whitelist for the key, ensure the current machine IP is allowed (or disable whitelist for testing).")
        print("- Ensure the API key has the required permissions (spot trading / trading enabled).")
        print("- If you are using Binance Testnet, use testnet endpoints or a testnet key.")
        print("- Make sure your system clock is accurate (signature errors can occur if clock skew is large).")
    else:
        print("See the raw error above. If this persists, enable debug logging and verify credentials and network connectivity.")


def main():
    setup_logger()

    # Load .env from project root (same folder as this cli.py)
    pkg_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(pkg_dir, ".env")
    load_dotenv(dotenv_path)

    parser = argparse.ArgumentParser()

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=False)

    args = parser.parse_args()

    print_api_key_status()

    try:
        validate_order(args.symbol, args.side, args.type, args.quantity, args.price)

        client = get_client()

        order = place_order(
            client,
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
        )

        print("\n✅ Order Summary")
        print(f"Symbol: {args.symbol}")
        print(f"Side: {args.side}")
        print(f"Type: {args.type}")
        print(f"Quantity: {args.quantity}")

        print("\n📊 Response")
        print(f"Order ID: {order.get('orderId')}")
        print(f"Status: {order.get('status')}")
        print(f"Executed Qty: {order.get('executedQty')}")
        print(f"Avg Price: {order.get('avgPrice')}")

    except Exception as e:
        handle_binance_error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()