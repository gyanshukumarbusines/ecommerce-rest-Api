from flask import Blueprint, request, jsonify
from backend.models import db, Product, Category

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id')
    search_query = request.args.get('q')
    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    products = query.all()
    return jsonify([{
        "id": p.id, "name": p.name, "description": p.description, "price": p.price,
        "stock": p.stock, "image_url": p.image_url, "category_id": p.category_id
    } for p in products]), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id, "name": product.name, "description": product.description,
        "price": product.price, "stock": product.stock, "image_url": product.image_url,
        "category_id": product.category_id
    }), 200

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name, "description": c.description} for c in categories]), 200
