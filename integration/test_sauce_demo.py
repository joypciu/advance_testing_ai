from playwright.sync_api import Page, expect
from tests.utils import setup_logging
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Set up logging
logger = setup_logging()

# Load environment variables and configure Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create the client
client = genai.Client(api_key=GEMINI_API_KEY)

class TestSauceDemoIntegration:
    def setup_method(self):
        """Setup test data for AI analysis"""
        self.test_data = {
            "user_journey": [],
            "ui_elements": [],
            "business_validation": [],
            "timestamp": datetime.now().isoformat()
        }

    def ai_analyze(self, prompt, analysis_type, max_tokens=250):
        """Helper method to get AI analysis"""
        try:
            print(f"\n🤖 AI {analysis_type.upper()} ANALYSIS:")
            print("-" * 50)
            
            response = client.models.generate_content(
                model='gemma-3n-e2b-it',
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7
                )
            )
            
            print(response.text)
            print("-" * 50)
            return response.text
        except Exception as e:
            print(f"❌ AI Analysis Error: {str(e)}")
            return f"AI Analysis failed: {str(e)}"

    def test_complete_purchase_flow_with_ai_integration(self, page: Page):
        """Complete purchase flow with comprehensive AI integration analysis"""
        print("\n🚀 STARTING AI-ENHANCED INTEGRATION TEST")
        
        # Step 1: Login with AI validation
        print("\n📍 STEP 1: LOGIN PROCESS")
        page.goto("https://www.saucedemo.com/")
        
        # Capture login page elements for AI analysis
        login_elements = {
            "username_field": page.locator("[data-test='username']").is_visible(),
            "password_field": page.locator("[data-test='password']").is_visible(),
            "login_button": page.locator("[data-test='login-button']").is_visible(),
            "page_title": page.title(),
            "url": page.url
        }
        
        # AI Analysis of Login Page
        login_prompt = f"""
        As a QA integration testing expert, analyze this login page structure:
        Elements present: {login_elements}
        
        Evaluate:
        1. UI completeness and accessibility
        2. Security considerations
        3. User experience flow
        4. Integration readiness
        5. Potential failure points
        
        Rate overall integration quality (1-10) and suggest improvements.
        """
        
        login_analysis = self.ai_analyze(login_prompt, "LOGIN PAGE")
        self.test_data["user_journey"].append({"step": "login", "analysis": login_analysis})
        
        # Perform login
        page.fill("[data-test='username']", "standard_user")
        page.fill("[data-test='password']", "secret_sauce")
        page.click("[data-test='login-button']")
        
        # Verify login success
        expect(page.locator("[data-test='title']")).to_be_visible()
        
        # Step 2: Product Catalog Analysis
        print("\n📍 STEP 2: PRODUCT CATALOG INTEGRATION")
        
        # Gather product data
        product_names = page.locator(".inventory_item_name").all_text_contents()
        product_prices = page.locator(".inventory_item_price").all_text_contents()
        product_count = len(product_names)
        
        catalog_data = {
            "product_count": product_count,
            "products": list(zip(product_names, product_prices)),
            "page_url": page.url
        }
        
        catalog_prompt = f"""
        As an e-commerce integration specialist, analyze this product catalog:
        {json.dumps(catalog_data, indent=2)}
        
        Evaluate:
        1. Product data integrity and consistency
        2. Pricing format and validation
        3. Catalog completeness
        4. User browsing experience
        5. Integration with backend systems
        6. Performance implications
        
        Identify any data inconsistencies or integration issues.
        """
        
        catalog_analysis = self.ai_analyze(catalog_prompt, "PRODUCT CATALOG")
        self.test_data["business_validation"].append({"step": "catalog", "analysis": catalog_analysis})
        
        # Step 3: Shopping Cart Integration
        print("\n📍 STEP 3: SHOPPING CART INTEGRATION")
        
        # Add items and track cart behavior
        initial_cart_count = page.locator("[data-test='shopping-cart-badge']").count()
        
        page.click("[data-test='add-to-cart-sauce-labs-backpack']")
        page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
        
        # Verify cart updates
        expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("2")
        final_cart_count = page.locator("[data-test='shopping-cart-badge']").text_content()
        
        cart_behavior = {
            "initial_count": initial_cart_count,
            "final_count": final_cart_count,
            "items_added": 2,
            "cart_update_successful": final_cart_count == "2"
        }
        
        cart_prompt = f"""
        As a frontend-backend integration expert, analyze this cart behavior:
        {json.dumps(cart_behavior, indent=2)}
        
        Evaluate:
        1. Real-time cart updates and synchronization
        2. State management between UI and backend
        3. Cart persistence and session handling
        4. User feedback mechanisms
        5. Error handling for cart operations
        6. Integration reliability
        
        Assess if cart integration follows best practices.
        """
        
        cart_analysis = self.ai_analyze(cart_prompt, "CART INTEGRATION")
        self.test_data["ui_elements"].append({"step": "cart", "analysis": cart_analysis})
        
        # Navigate to cart
        page.click(".shopping_cart_link")
        
        # Step 4: Checkout Process Integration
        print("\n📍 STEP 4: CHECKOUT INTEGRATION")
        
        # Capture checkout items
        cart_items = page.locator(".cart_item").count()
        
        page.click("[data-test='checkout']")
        
        # Analyze checkout form
        checkout_fields = {
            "firstName_required": page.locator("[data-test='firstName']").is_visible(),
            "lastName_required": page.locator("[data-test='lastName']").is_visible(),
            "postalCode_required": page.locator("[data-test='postalCode']").is_visible(),
            "form_validation": "pending",
            "items_in_checkout": cart_items
        }
        
        checkout_prompt = f"""
        As a payment integration and UX specialist, analyze this checkout process:
        {json.dumps(checkout_fields, indent=2)}
        
        Evaluate:
        1. Form validation and error handling
        2. Data collection completeness
        3. User experience and friction points
        4. Integration with payment systems
        5. Security considerations
        6. Mobile responsiveness
        7. Checkout abandonment risks
        
        Rate the checkout integration quality and suggest optimizations.
        """
        
        checkout_analysis = self.ai_analyze(checkout_prompt, "CHECKOUT PROCESS")
        self.test_data["business_validation"].append({"step": "checkout", "analysis": checkout_analysis})
        
        # Fill checkout form
        page.fill("[data-test='firstName']", "Test")
        page.fill("[data-test='lastName']", "User")
        page.fill("[data-test='postalCode']", "12345")
        page.click("[data-test='continue']")
        
        # Step 5: Order Summary and Completion
        print("\n📍 STEP 5: ORDER COMPLETION INTEGRATION")
        
        # Capture order summary data
        try:
            order_total = page.locator(".summary_total_label").text_content()
            tax_amount = page.locator(".summary_tax_label").text_content()
        except:
            order_total = "Not captured"
            tax_amount = "Not captured"
        
        order_data = {
            "order_total": order_total,
            "tax_calculation": tax_amount,
            "page_url": page.url,
            "completion_ready": True
        }
        
        # Complete purchase
        page.click("[data-test='finish']")
        
        # Verify success
        success_message = page.locator(".complete-header").text_content()
        expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")
        
        # Final integration analysis
        completion_data = {
            "success_message": success_message,
            "order_summary": order_data,
            "transaction_completed": success_message == "Thank you for your order!"
        }
        
        completion_prompt = f"""
        As a full-stack integration expert, analyze this order completion:
        {json.dumps(completion_data, indent=2)}
        
        Provide a comprehensive integration assessment:
        1. End-to-end transaction integrity
        2. Data flow consistency across all steps
        3. Error handling and recovery mechanisms
        4. User experience continuity
        5. Business logic validation
        6. System reliability indicators
        7. Integration testing coverage gaps
        
        Give an overall integration health score (1-100) and critical recommendations.
        """
        
        completion_analysis = self.ai_analyze(completion_prompt, "ORDER COMPLETION", 300)
        self.test_data["business_validation"].append({"step": "completion", "analysis": completion_analysis})
        
        # Generate comprehensive test report
        self.generate_ai_integration_report()
        
        print("✅ AI-ENHANCED INTEGRATION TEST COMPLETED!")

    def test_product_analysis_with_gemini(self, page: Page):
        """Enhanced product analysis for integration testing"""
        print("\n🎯 PRODUCT INTEGRATION ANALYSIS TEST")
        
        try:
            # Navigate and login
            page.goto("https://www.saucedemo.com/")
            page.fill("[data-test='username']", "standard_user")
            page.fill("[data-test='password']", "secret_sauce")
            page.click("[data-test='login-button']")
            
            # Get all product data for comprehensive analysis
            products = []
            product_elements = page.locator(".inventory_item").all()
            
            for i, product in enumerate(product_elements[:3]):  # Analyze first 3 products
                name = product.locator(".inventory_item_name").text_content()
                desc = product.locator(".inventory_item_desc").text_content()
                price = product.locator(".inventory_item_price").text_content()
                
                products.append({
                    "name": name,
                    "description": desc,
                    "price": price
                })
                
                print(f"\n🔍 ANALYZING PRODUCT {i+1}: {name}")
                print(f"💰 PRICE: {price}")
                print(f"📝 DESCRIPTION: {desc}")
            
            # Comprehensive product integration analysis
            integration_prompt = f"""
            As a product management and e-commerce integration expert, analyze these products:
            {json.dumps(products, indent=2)}
            
            Provide integration-focused analysis:
            1. Product data consistency across catalog
            2. Pricing strategy and format validation
            3. Description quality and SEO optimization
            4. Product categorization and taxonomy
            5. Integration with inventory management
            6. Customer segmentation alignment
            7. Cross-selling and upselling opportunities
            8. A/B testing recommendations
            
            Rate overall product integration maturity (1-10) and provide actionable insights.
            """
            
            analysis = self.ai_analyze(integration_prompt, "PRODUCT INTEGRATION", 400)
            
            # Verify meaningful integration analysis
            integration_keywords = ['integration', 'data', 'consistency', 'catalog', 'inventory', 'management']
            assert any(keyword in analysis.lower() for keyword in integration_keywords), \
                "Analysis should contain integration-focused insights"
            
            print("✅ PRODUCT INTEGRATION ANALYSIS COMPLETED!")
            
        except Exception as e:
            print(f"❌ ERROR in product integration analysis: {str(e)}")
            logger.error(f"Error in product integration analysis: {str(e)}")
            raise

    def generate_ai_integration_report(self):
        """Generate comprehensive AI-powered integration test report"""
        print("\n📊 GENERATING AI INTEGRATION REPORT")
        
        report_prompt = f"""
        As a senior QA integration testing consultant, analyze this complete test data:
        {json.dumps(self.test_data, indent=2)}
        
        Generate a comprehensive integration test report:
        
        EXECUTIVE SUMMARY:
        - Overall integration health score (1-100)
        - Critical issues identified
        - Risk assessment
        
        TECHNICAL FINDINGS:
        - Frontend-backend integration quality
        - Data flow consistency
        - Error handling effectiveness
        - Performance implications
        
        BUSINESS IMPACT:
        - User experience assessment  
        - Revenue impact factors
        - Conversion optimization opportunities
        
        RECOMMENDATIONS:
        - Priority fixes needed
        - Integration improvements
        - Testing strategy enhancements
        
        Provide actionable insights for development and QA teams.
        """
        
        report = self.ai_analyze(report_prompt, "INTEGRATION REPORT", 500)
        
        # Save report to file
        try:
            with open("ai_integration_report.md", "w") as f:
                f.write(f"# AI Integration Test Report\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Analysis\n\n{report}\n\n")
                f.write(f"## Raw Test Data\n\n```json\n{json.dumps(self.test_data, indent=2)}\n```")
            print("📄 Integration report saved to: ai_integration_report.md")
        except Exception as e:
            print(f"⚠️  Could not save report file: {e}")
        
        return report