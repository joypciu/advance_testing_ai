from playwright.sync_api import Page, expect
import requests

class TestSecurity:
    def test_xss_prevention(self, page: Page):
        # Test XSS prevention in input fields
        xss_payload = "<script>alert('xss')</script>"
        
        page.goto("https://www.saucedemo.com/")
        page.fill("[data-test='username']", xss_payload)
        page.fill("[data-test='password']", "secret_sauce")
        page.click("[data-test='login-button']")
        
        # Verify XSS payload is not executed
        page_content = page.content()
        assert xss_payload not in page_content, "XSS payload should be escaped"
    
    def test_sql_injection_prevention(self, page: Page):
        # Test SQL injection prevention
        sql_injection = "' OR '1'='1"
        
        page.goto("https://www.saucedemo.com/")
        page.fill("[data-test='username']", sql_injection)
        page.fill("[data-test='password']", sql_injection)
        page.click("[data-test='login-button']")
        
        # Verify login fails
        expect(page.locator("[data-test='error']")).to_be_visible()
    
    def test_csrf_protection(self, page: Page):
        # Test CSRF protection by attempting to submit forms with invalid/missing tokens
        # Note: This is a basic example, actual implementation would depend on the site's CSRF protection
        
        page.goto("https://www.saucedemo.com/")
        page.fill("[data-test='username']", "standard_user")
        page.fill("[data-test='password']", "secret_sauce")
        page.click("[data-test='login-button']")
        
        # Attempt direct POST request to checkout endpoint
        response = requests.post(
            "https://www.saucedemo.com/checkout-step-one.html",
            data={"firstName": "Test", "lastName": "User", "postalCode": "12345"}
        )
        
        # Verify direct POST is not successful
        assert response.status_code != 200, "Direct POST should not be allowed"
