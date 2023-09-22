from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()
PRODUCTS_URL = os.getenv('PRODUCTS_URL')
print('GAAAAAAH\n\n')
print(PRODUCTS_URL)

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
@app.route("/cart/<int:user_id>/add/<int:product_id>", methods=["POST"])
def retrieve_product(user_id, product_id):
  product = requests.get(f'{PRODUCTS_URL}/products/{product_id}')  # Check if product exists
  if product:
    product_object = {
       "id": product_id,
       "quantity": request.json.get('quantity')
    }
    retrieved_product = requests.post(f'{PRODUCTS_URL}/products/retrieve', json=product_object)
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
# Logic here assumes that products that exist in the product service can hold virtually infinite supplies
@app.route("/cart/<int:user_id>/remove/<int:product_id>", methods=["POST"])
def return_product(user_id, product_id):
  product = requests.get(f'{PRODUCTS_URL}/products/{product_id}')  # Check if product exists
  if product:
    product_object = {
       "id": product_id,
       "quantity": request.json.get('quantity')
    }
    if product_object['quantity'] < 1:
      return jsonify('Must remove one or more of quantity')
    cart = next((cart for cart in carts if cart['user'] == user_id), None)
    valid_product = False
    # Check if product exists IN CART
    for cart_product in cart['products']:
      if cart_product['id'] == product_id:
        valid_product = True
        temp = cart_product['quantity']
        cart_product['quantity'] -= product_object['quantity']  # Lower quantity in cart
        if cart_product['quantity'] <= 0:
            cart['products'].remove(cart_product)
            # If user tries returning higher quantity than what is in cart, then return all of the given product
            if cart_product['quantity'] < 0:
              product_object['quantity'] = temp
        break
    if valid_product:
      requests.post(f'{PRODUCTS_URL}/products/return', json=product_object)
    else:
       return jsonify({'Cart Unchanged': 'User did not have that product'})
    return jsonify({'Cart': cart['products']})
  else:
     return jsonify({"Cart unchanged": "Product does not exist"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
