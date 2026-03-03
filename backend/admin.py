from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import db, Product, Category, Order, User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.rolefrom flask import Blueprint, request, jsonify
 != 'admin':
        return jsonify({"message": "Admin access required"}), 403
    data = request.get_json()
    product = Product(name=data['name'], description=data.get('description'), price=data['price'], stock=data.get('stock', 0), image_url=data.get('image_url'), category_id=data['category_id'])
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added", "id": product.id}), 201

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({"message": "Admin access required"}), 403
    orders = Order.query.all()
    return jsonify([{
        "id": o.id, "user_email": o.user.email, "total_amount": o.total_amount, "status": o.status, "created_at": o.created_at
    } for o in orders]), 200

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({"message": "Admin access required"}), 403
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    order_count = Order.query.count()
    product_count = Product.query.count()
    user_count = User.query.count()
    return jsonify({"total_sales": total_sales, "order_count": order_count, "product_count": product_count, "user_count": user_count}), 200
