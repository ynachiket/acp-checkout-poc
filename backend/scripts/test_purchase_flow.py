"""
End-to-End Purchase Flow Test Script

Demonstrates the complete purchase flow through the ACP API.
This script tests all major endpoints and shows the full user journey.

Usage:
    python scripts/test_purchase_flow.py
"""

import requests
import json
import time
from typing import Dict
from decimal import Decimal


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class PurchaseFlowTester:
    """Test the complete purchase flow."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
        self.payment_token = None
        self.order_id = None
    
    def print_header(self, text: str):
        """Print section header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    def print_step(self, step: int, text: str):
        """Print step indicator."""
        print(f"{Colors.BLUE}{Colors.BOLD}Step {step}: {text}{Colors.END}")
    
    def print_success(self, text: str):
        """Print success message."""
        print(f"{Colors.GREEN}✅ {text}{Colors.END}")
    
    def print_error(self, text: str):
        """Print error message."""
        print(f"{Colors.RED}❌ {text}{Colors.END}")
    
    def print_info(self, text: str):
        """Print info message."""
        print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")
    
    def print_json(self, data: Dict, indent: int = 2):
        """Print formatted JSON."""
        print(json.dumps(data, indent=indent))
    
    def test_health_check(self) -> bool:
        """Test 0: Health check."""
        self.print_step(0, "Health Check")
        
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            
            data = response.json()
            self.print_success(f"API is healthy: {data['status']}")
            self.print_info(f"App: {data['app']}")
            self.print_info(f"Version: {data['version']}")
            return True
        
        except Exception as e:
            self.print_error(f"Health check failed: {e}")
            self.print_info("Make sure the server is running: uvicorn app.main:app --reload")
            return False
    
    def test_create_checkout_session(self) -> bool:
        """Test 1: Create checkout session."""
        self.print_step(1, "Create Checkout Session")
        
        payload = {
            "line_items": [
                {
                    "gtin": "00883419552502",  # Nike Air Max 90
                    "quantity": 1
                }
            ],
            "fulfillment_address": {
                "name": "John Doe",
                "address_line_1": "123 Main St",
                "address_line_2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US"
            },
            "buyer_info": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+12125551234"
            }
        }
        
        try:
            self.print_info("Creating checkout session with Nike Air Max 90...")
            response = requests.post(
                f"{self.base_url}/acp/v1/checkout_sessions",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            self.session_id = data["id"]
            
            self.print_success(f"Session created: {self.session_id}")
            self.print_info(f"Status: {data['status']}")
            self.print_info(f"Total: ${data['totals']['total']['value']}")
            
            # Print line items
            print("\n📦 Items in cart:")
            for item in data["line_items"]:
                print(f"   - {item['title']} (qty: {item['quantity']}) - ${item['total']}")
            
            # Print shipping options
            print("\n🚚 Shipping options:")
            for option in data["fulfillment_options"]:
                selected = "✓" if option["id"] == data["selected_fulfillment_option_id"] else " "
                print(f"   [{selected}] {option['title']} - ${option['cost']} ({option['subtitle']})")
            
            # Print totals breakdown
            totals = data["totals"]
            print("\n💰 Price breakdown:")
            print(f"   Items:    ${totals['items_total']['value']}")
            print(f"   Shipping: ${totals['fulfillment']['value']}")
            print(f"   Tax:      ${totals['taxes']['value']}")
            print(f"   ─────────────────────")
            print(f"   Total:    ${totals['total']['value']}")
            
            return True
        
        except Exception as e:
            self.print_error(f"Failed to create session: {e}")
            return False
    
    def test_get_checkout_session(self) -> bool:
        """Test 2: Get checkout session."""
        self.print_step(2, "Retrieve Checkout Session")
        
        if not self.session_id:
            self.print_error("No session ID available")
            return False
        
        try:
            self.print_info(f"Fetching session: {self.session_id}")
            response = requests.get(
                f"{self.base_url}/acp/v1/checkout_sessions/{self.session_id}"
            )
            response.raise_for_status()
            
            data = response.json()
            self.print_success(f"Session retrieved successfully")
            self.print_info(f"Status: {data['status']}")
            self.print_info(f"Total: ${data['totals']['total']['value']}")
            
            return True
        
        except Exception as e:
            self.print_error(f"Failed to get session: {e}")
            return False
    
    def test_update_checkout_session(self) -> bool:
        """Test 3: Update checkout session (change shipping)."""
        self.print_step(3, "Update Shipping Option")
        
        if not self.session_id:
            self.print_error("No session ID available")
            return False
        
        try:
            self.print_info("Changing to Express Shipping...")
            payload = {
                "selected_fulfillment_option_id": "express"
            }
            
            response = requests.post(
                f"{self.base_url}/acp/v1/checkout_sessions/{self.session_id}",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            self.print_success("Shipping option updated")
            self.print_info(f"New shipping: ${data['totals']['fulfillment']['value']}")
            self.print_info(f"New total: ${data['totals']['total']['value']}")
            
            return True
        
        except Exception as e:
            self.print_error(f"Failed to update session: {e}")
            return False
    
    def test_delegate_payment(self) -> bool:
        """Test 4: Tokenize payment."""
        self.print_step(4, "Tokenize Payment Information")
        
        payload = {
            "card_number": "4242424242424242",
            "exp_month": 12,
            "exp_year": 2025,
            "cvc": "123",
            "billing_address": {
                "address_line_1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US"
            }
        }
        
        try:
            self.print_info("Tokenizing card: 4242 4242 4242 4242")
            response = requests.post(
                f"{self.base_url}/acp/v1/delegate_payment",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            self.payment_token = data["payment_token_id"]
            
            self.print_success(f"Payment tokenized: {self.payment_token}")
            self.print_info("💳 Using test card (mock for POC)")
            
            return True
        
        except Exception as e:
            self.print_error(f"Failed to tokenize payment: {e}")
            return False
    
    def test_complete_checkout(self) -> bool:
        """Test 5: Complete the purchase."""
        self.print_step(5, "Complete Purchase")
        
        if not self.session_id or not self.payment_token:
            self.print_error("Missing session ID or payment token")
            return False
        
        try:
            self.print_info("Processing payment and creating order...")
            payload = {
                "payment_token_id": self.payment_token
            }
            
            response = requests.post(
                f"{self.base_url}/acp/v1/checkout_sessions/{self.session_id}/complete",
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            self.order_id = data["order"]["id"]
            
            self.print_success("🎉 Purchase completed successfully!")
            self.print_success(f"Order ID: {self.order_id}")
            self.print_info(f"Order link: {data['order']['permalink']}")
            
            # Print confirmation message
            if data.get("messages"):
                print(f"\n📧 {data['messages'][0]['text']}")
            
            return True
        
        except Exception as e:
            self.print_error(f"Failed to complete checkout: {e}")
            if hasattr(e, 'response'):
                try:
                    error_detail = e.response.json()
                    self.print_info(f"Error details: {error_detail}")
                except:
                    pass
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests in sequence."""
        self.print_header("NIKE AGENTIC COMMERCE POC - PURCHASE FLOW TEST")
        
        print(f"{Colors.BOLD}Testing complete purchase flow from cart to order confirmation{Colors.END}")
        print(f"Base URL: {self.base_url}\n")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Create Checkout Session", self.test_create_checkout_session),
            ("Retrieve Session", self.test_get_checkout_session),
            ("Update Shipping", self.test_update_checkout_session),
            ("Tokenize Payment", self.test_delegate_payment),
            ("Complete Purchase", self.test_complete_checkout),
        ]
        
        results = []
        
        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
                
                if not result:
                    self.print_error(f"Test failed: {name}")
                    break
                
                # Small delay between tests
                time.sleep(0.5)
            
            except KeyboardInterrupt:
                self.print_info("\nTest interrupted by user")
                break
            except Exception as e:
                self.print_error(f"Unexpected error in {name}: {e}")
                results.append((name, False))
                break
        
        # Print summary
        self.print_header("TEST SUMMARY")
        
        total = len(results)
        passed = sum(1 for _, result in results if result)
        
        print(f"\n{Colors.BOLD}Results:{Colors.END}")
        for name, result in results:
            status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
            print(f"  {status} - {name}")
        
        print(f"\n{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Total tests: {total}")
        print(f"  Passed: {Colors.GREEN}{passed}{Colors.END}")
        print(f"  Failed: {Colors.RED}{total - passed}{Colors.END}")
        
        if passed == total:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! The purchase flow is working correctly.{Colors.END}\n")
            
            if self.order_id:
                print(f"{Colors.BOLD}Order Details:{Colors.END}")
                print(f"  Order ID: {self.order_id}")
                print(f"  Session ID: {self.session_id}")
                print(f"  Status: Completed ✅\n")
            
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.END}\n")
            return False


def main():
    """Main entry point."""
    import sys
    
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = PurchaseFlowTester(base_url)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

