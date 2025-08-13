from locust import HttpUser, task, between
import json
import random

class WebsiteLoadTest(HttpUser):
    """
    A Locust user class for load testing web applications.
    This template can be adapted for testing any website with similar flows.
    """
    
    # Basic configuration
    host = "https://www.saucedemo.com"  # Replace with your target website
    wait_time = between(1, 3)  # Random wait between 1-3 seconds between tasks
    
    # Test data (you can modify these for your website)
    test_credentials = {
        "username": "standard_user",
        "password": "secret_sauce"
    }
    
    def __init__(self, *args, **kwargs):
        """Initialize user session variables"""
        super().__init__(*args, **kwargs)
        self.session_token = None
        self.cart_items = []
    
    def on_start(self):
        """
        Execute on start of each user simulation.
        Typically used for login and initial setup.
        """
        # 1. Get the login page first (often needed to get cookies/tokens)
        self.client.get("/")
            
        # 2. Perform login
        login_data = {
            "user-name": self.test_credentials["username"],
            "password": self.test_credentials["password"]
        }
        
        # Add headers to mimic browser behavior (important for security-conscious sites)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        
        # Perform login and check response
        response = self.client.post("/login", data=login_data, headers=headers)
        if response.status_code != 200:
            print(f"Login failed with status code: {response.status_code}")
    
    @task(3)  # Weight of 3 means this task runs more frequently
    def browse_products(self):
        """
        Simulate user browsing products.
        This is typically one of the most common user actions.
        """
        with self.client.get("/inventory.html", name="View Products", catch_response=True) as response:
            if response.status_code != 200:
                print(f"Failed to browse products: {response.status_code}")
    
    @task(2)
    def product_search(self):
        """
        Simulate product search behavior.
        Adapt the search parameters for your website.
        """
        search_terms = ["shirt", "jacket", "pants"]  # Example search terms
        term = random.choice(search_terms)
        
        params = {"q": term}
        with self.client.get(
            "/inventory.html",
            params=params,
            name=f"Search Products",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                print(f"Search failed: {response.status_code}")
    
    @task(1)
    def add_to_cart(self):
        """
        Simulate adding items to cart.
        Adapt the product IDs and data structure for your website.
        """
        product_ids = ["4", "5", "6"]  # Example product IDs
        product_id = random.choice(product_ids)
        
        # Some sites use POST for adding to cart, others use GET with parameters
        with self.client.post(
            f"/cart-add/{product_id}",
            name="Add to Cart",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                self.cart_items.append(product_id)
            else:
                print(f"Failed to add item to cart: {response.status_code}")
    
    @task(1)
    def checkout_process(self):
        """
        Simulate complete checkout process.
        This is typically a multi-step process with several requests.
        """
        if not self.cart_items:  # Skip if cart is empty
            return
            
        # Step 1: View Cart
        response = self.client.get("/cart.html", name="View Cart")
        if response.status_code != 200:
            print("Failed to view cart")
            return
        
        # Step 2: Start Checkout
        response = self.client.get("/checkout-step-1.html", name="Start Checkout")
        if response.status_code != 200:
            print("Could not start checkout")
            return
        
        # Step 3: Submit Shipping Information
        shipping_info = {
            "firstName": "Test",
            "lastName": "User",
            "postalCode": "12345"
        }
        
        response = self.client.post(
            "/checkout-step-1.html",
            data=shipping_info,
            name="Submit Shipping Info"
        )
        if response.status_code != 200:
            print("Failed to submit shipping info")
            return
        
        # Step 4: Review Order
        response = self.client.get("/checkout-step-2.html", name="Review Order")
        if response.status_code != 200:
            print("Failed to review order")
            return
        
        # Step 5: Complete Order
        response = self.client.get("/checkout-complete.html", name="Complete Order")
        if response.status_code != 200:
            print("Failed to complete order")
            return
        
        # Reset cart after successful checkout
        self.cart_items = []
    
    def on_stop(self):
        """
        Execute when the user simulation stops.
        Use this for cleanup (logout, etc.)
        """
        # Example: Logout request
        self.client.get("/logout")  # Adjust endpoint as needed
