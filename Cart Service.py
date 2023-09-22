from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

carts = [
    {"user": 1, "products": [{'name': 'Froot Loops','price': 2.50, 'id': 1, 'quantity': 3}, {'name': 'Milk', 'price': 3.49, 'id': 2, 'quantity': 2}]},
    {"user": 2, "products": [{'name': 'Froot Loops','price': 2.50, 'id': 1, 'quantity': 1}, {'name': 'Milk', 'price': 3.49, 'id': 2, 'quantity': 1}]}
]

# View all carts; not required but I wanted to add it or completion sake
@app.route("/cart", methods=["GET"])
def check_carts():
   return jsonify(carts)

# Gets/views all products in a specified user's cart
@app.route("/cart/<int:user_id>", methods=["GET"])
def check_cart(user_id):
    cart = next((cart for cart in carts if cart['user'] == user_id), None)
    if cart:
      return jsonify({"User's Products": cart['products']})
    else:
        return jsonify({"Error": "User Cart Not Found"})

# Add a specified quantity of a product to a user's cart
# Return here; stuff broke; look into it more
@app.route("/cart/<int:user_id>/product/<int:product_id>", methods=["POST"])
def add_product(user_id, product_id):
  product = requests.get(f'http://127.0.0.1:5000/products/{product_id}')  # Check if product exists
  if product:
    product_object = {
       "name": request.json.get('name'),
       "quantity": request.json.get('quantity')
    }
    retrieved_product = requests.post('http://127.0.0.1:5000/products/retrieve', json=product_object)
    cart = next((cart for cart in carts if cart['user'] == user_id), None)
    already_in_cart = False  # Indicates if a given product is already in the cart
    for cart_product in cart['products']:
       if cart_product['id'] == product_id:
          cart_product['quantity'] += retrieved_product.json()['quantity']  # Increase existing quantity instead of appending product
          already_in_cart = True
          break
    if not already_in_cart:
      cart['products'].append(retrieved_product.json())
    return jsonify({'Cart': cart['products']})
  else:
     return jsonify({"Cart unchanged": "Product does not exist"})


# Remove a specified quantity of a product to a user's cart


if __name__ == '__main__':
    app.run(debug=True, port=5001)
