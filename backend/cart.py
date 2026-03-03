from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, CartItem, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": item.id, "product_id": item.product_id, "product_name": item.product.name,
        "quantity": item.quantity, "price": item.product.price, "image_url": item.product.image_url
    } for item in items]), 200

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({"message": "Not enough stock"}), 400
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Added to cart"}), 200

@cart_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200
