import requests

from flask import redirect, render_template, session
from functools import wraps


def error(message, code=400):
    return render_template("error.html", code=code, message=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

#inspired by finance
import requests

def live(symbol):
    """
    Return the current price as a float, or None if it fails.
    `symbol` can be 'BTC' or 'BTCUSDC'; we normalise it.
    """

    if not symbol:
        return None

    symbol = symbol.upper()

    # Avoid BTCUSDCUSDC if caller already included USDC
    if symbol.endswith("USDC"):
        query_symbol = symbol
    else:
        query_symbol = symbol + "USDC"

    pair = symbol.upper()
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        quote_data = response.json()
        price = float(quote_data["price"])
        return price

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"[live] Error fetching quote for {query_symbol}: {e}")
        return None
