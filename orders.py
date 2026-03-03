from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Order, OrderItem, CartItem

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    order = Order(user_id=user_id, total_amount=total_amount, status='completed')
    db.session.add(order)
    db.session.flush()
    for item in cart_items:
        if item.product.stock < item.quantity:
            db.session.rollback()
            return jsonify({"message": f"Not enough stock for {item.product.name}"}), 400
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price_at_time=item.product.price)
        item.product.stock -= item.quantity
        db.session.add(order_item)
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Order placed successfully", "order_id": order.id}), 201

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([{
        "id": o.id, "total_amount": o.total_amount, "status": o.status, "created_at": o.created_at,
        "items": [{"product_name": item.product.name, "quantity": item.quantity, "price": item.price_at_time} for item in o.items]
    } for o in orders]), 200
