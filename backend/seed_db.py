import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.models import db, Category, Product, User

def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        customer = User(username='johndoe', email='john@example.com', role='customer')
        customer.set_password('password123')
        db.session.add(customer)
        electronics = Category(name='Electronics', description='Gadgets and tech')
        fashion = Category(name='Fashion', description='Clothing and accessories')
        home = Category(name='Home & Living', description='Furniture and decor')
        db.session.add_all([electronics, fashion, home])
        db.session.flush()
        p1 = Product(name='Premium Wireless Headphones', description='High-quality noise-canceling headphones.', price=299.99, stock=50, image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800', category_id=electronics.id)
        p2 = Product(name='Modern Smartwatch', description='Sleek smartwatch with heart rate monitoring.', price=199.99, stock=30, image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800', category_id=electronics.id)
        p3 = Product(name='Luxury Leather Wallet', description='Handcrafted genuine leather wallet.', price=49.99, stock=100, image_url='https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=800', category_id=fashion.id)
        p4 = Product(name='Minimalist Ceramic Vase', description='Hand-painted ceramic vase.', price=35.00, stock=20, image_url='https://images.unsplash.com/photo-1581783898377-1c85bf937427?auto=format&fit=crop&w=800', category_id=home.id)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
