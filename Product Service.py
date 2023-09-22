from flask import Flask, jsonify, request
app = Flask(__name__)
from copy import copy

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

# Get all products and their info
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify({"Products": products})

# Get info on specific product based off product id
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_info(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        return jsonify({'product': product})
    else:
        return jsonify({'Error': "Product Not Found"}), 404

# Add new product to inventory
@app.route('/products', methods=['POST'])
def add_product():
    product = {
        'name': request.json.get('name'),
        'price': request.json.get('price'),
        'id': len(products) + 1,
        'quantity': request.json.get('quantity')
    }
    products.append(product)
    return jsonify({"New Product": product})


# From here on and below, endpoints will interact with the cart service
@app.route('/products/retrieve', methods=["POST"])
def retrieve_product():
    product_id = request.json.get('id')
    specified_quantity = request.json.get('quantity')
    if (specified_quantity == None):
        specified_quantity = 1
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        purchased_product = copy(product)
        purchased_product['quantity'] = 0
        counter = 0
        # Remove one item at a time in case user tries getting more than available
        while counter < specified_quantity: 
          if product['quantity'] > 0:
            product['quantity'] = product['quantity'] - 1
            purchased_product['quantity'] = purchased_product['quantity'] + 1
          else:
            if counter == 0:
              return jsonify(product), 410  # Product completely out of stock
            return jsonify(purchased_product), 206  # User asked for more than what was in stock
          counter += 1
        return jsonify(purchased_product)  # Successfully added desired quantity
    else:
        return jsonify({"Error": "Product Not Found"}), 404

# Return product from cart back to shelf
@app.route('/products/return', methods=["POST"])
def return_product():
  product_id = request.json.get('id')
  specified_quantity = request.json.get('quantity')
  for product in products:
    if product['id'] == product_id:
      product['quantity'] += specified_quantity
      break
  return jsonify('Products returned')

if __name__ == '__main__':
    app.run(debug=True)
