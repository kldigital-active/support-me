import os
import requests
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)

# -----------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------
# Put your Yoco SECRET key here (test key while developing, e.g. starts with sk_test_...)
# Get it from: Yoco Business Portal > Settings > Online Payments / Checkout API > API Keys
YOCO_SECRET_KEY = os.environ.get("YOCO_SECRET_KEY", "sk_live_PUT_YOUR_TEST_KEY_HERE")

# Where Yoco should send the customer back to after paying.
# While running locally, this is just localhost. Update this when you deploy.
BASE_URL = os.environ.get("BASE_URL", "https://support-me-4ze4.onrender.com")

YOCO_CHECKOUT_URL = "https://payments.yoco.com/api/checkouts"

# In-memory store of checkout statuses, just for this demo.
# (Good enough for local testing - swap for a real DB if you deploy this for real.)
checkouts = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create-checkout", methods=["POST"])
def create_checkout():
    """
    Called from the page when someone enters an amount and clicks Pay.
    We create a Checkout session with Yoco from OUR SERVER (never from the browser,
    because that's the only place the secret key is allowed to live), then send
    the redirect URL back to the browser so it can send the customer to Yoco's
    secure hosted payment page.
    """
    data = request.get_json()

    try:
        rand_amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Please enter a valid amount."}), 400

    if rand_amount < 2:
        return jsonify({"error": "Minimum payment is R2."}), 400

    amount_in_cents = int(round(rand_amount * 100))

    payload = {
        "amount": amount_in_cents,
        "currency": "ZAR",
        "successUrl": f"{BASE_URL}/success",
        "cancelUrl": f"{BASE_URL}/",
        "failureUrl": f"{BASE_URL}/",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YOCO_SECRET_KEY}",
    }

    try:
        resp = requests.post(YOCO_CHECKOUT_URL, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        detail = ""
        if e.response is not None:
            detail = e.response.text
        return jsonify({"error": "Could not start checkout.", "detail": detail}), 502

    checkout = resp.json()
    checkout_id = checkout.get("id")
    redirect_url = checkout.get("redirectUrl")

    if checkout_id:
        checkouts[checkout_id] = "created"

    return jsonify({"redirectUrl": redirect_url})


@app.route("/success")
def success():
    """
    Yoco redirects the customer's browser here after a successful payment.
    NOTE: successUrl alone is not proof of payment (Yoco says don't rely on it
    for verification) - for a real production version you'd verify with a
    webhook on your server before treating this as final. For this local/demo
    version, landing here is enough to show the thank-you page.
    """
    return render_template("success.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
