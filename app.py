import os
import json
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

STUDIO_EMAIL = "creativedesigntpy@gmail.com"
STUDIO_PHONE = "910-674-7501"

def load_inventory():
    if os.path.exists("inventory.json"):
        with open("inventory.json", "r") as f:
            return json.load(f)
    return []

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    return jsonify(load_inventory())

@app.route("/api/checkout", methods=["POST"])
def backend_checkout():
    data = request.get_json()
    if not data or not data.get("cart"):
        return jsonify({"error": "Cart is empty"}), 400
    
    order_id = f"SMI-{random.randint(1000, 9999)}"
    inventory = load_inventory()
    inv_map = {item["id"]: item for item in inventory}
    
    calculated_total = 0.0
    for cart_item in data["cart"]:
        item_id = cart_item.get("id")
        opt_index = cart_item.get("optionIndex", 0)
        
        if item_id in inv_map:
            prod = inv_map[item_id]
            option = prod["options"][opt_index]
            calculated_total += option["price"]

    if data.get("delivery") == "shipping":
        calculated_total += 6.00

    return jsonify({
        "status": "success",
        "orderId": order_id,
        "total": round(calculated_total, 2),
        "payMethod": data.get("payMethod", "PayPal"),
        "studioEmail": STUDIO_EMAIL,
        "studioPhone": STUDIO_PHONE
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)