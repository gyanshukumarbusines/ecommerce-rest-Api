import requests

BASE_URL = "http://localhost:5000/api"

def test_flow():
    print("Testing API Flow...")
    
    # 1. Health Check
    res = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {res.status_code} - {res.json()}")
    
    # 2. Get Products
    res = requests.get(f"{BASE_URL}/products")
    print(f"Get Products: {res.status_code} - Found {len(res.json())} products")
    
    # 3. Login
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "john@example.com",
        "password": "password123"
    })
    print(f"Login (Customer): {res.status_code}")
    token = res.json().get('access_token')
    
    # 4. Add to Cart
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/cart/add", headers=headers, json={
        "product_id": 1,
        "quantity": 1
    })
    print(f"Add to Cart: {res.status_code} - {res.json()}")
    
    # 5. Get Cart
    res = requests.get(f"{BASE_URL}/cart", headers=headers)
    print(f"Get Cart: {res.status_code} - Items: {len(res.json())}")
    
    # 6. Checkout
    res = requests.post(f"{BASE_URL}/orders/checkout", headers=headers)
    print(f"Checkout: {res.status_code} - {res.json()}")
    
    # 7. Admin Check
    admin_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@example.com",
        "password": "admin123"
    })
    admin_token = admin_res.json().get('access_token')
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    res = requests.get(f"{BASE_URL}/admin/stats", headers=admin_headers)
    print(f"Admin Stats: {res.status_code} - {res.json()}")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Test failed: {e}")
