from flask import Flask, jsonify, request
app = Flask(__name__)

# Sorry for not being ambitious by not using a DB, but I am busy and need to complete this asap
products = [
    {'name': 'Froot Loops','price': 2.50, 'id': 1, 'quantity': 20},
    {'name': 'Milk', 'price': 3.49, 'id': 2, 'quantity': 48},
    {'name': 'Whipped Cream', 'price': 1.79, 'id': 3, 'quantity': 8},
    {'name': "Digiorno's Pizza", 'price': 6.80, 'id': 4, 'quantity': 30},
    {'name': 'Canned Spinach', 'price': 0.89, 'id': 5, 'quantity': 16},
    {'name': 'Oatmeal Creme Pies', 'price': 5.00, 'id': 6, 'quantity': 12},
    {'name': 'Black Forest Ham', 'price': 4.39, 'id': 7, 'quantity': 8},
    {'name': 'Wonder Bread', 'price': 1.25, 'id': 8, 'quantity': 12},
    {'name': 'Rainbow Cookies', 'price': 5.99, 'id': 9, 'quantity': 10},
    {'name': 'Animal Crackers', 'price': 0.50, 'id': 10, 'quantity': 24}
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"Products": products})


if __name__ == '__main__':
    app.run(debug=True)
