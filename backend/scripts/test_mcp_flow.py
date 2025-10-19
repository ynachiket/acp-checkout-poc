"""
MCP Protocol Demo Script

Demonstrates the complete purchase flow using MCP tools instead of REST API.
This shows how AI agents would interact with the commerce system.
"""

import requests
import json
from typing import Dict


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class MCPFlowTester:
    """Test the complete flow using MCP protocol."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.mcp_endpoint = f"{base_url}/mcp"
        self.request_id = 1
    
    def call_mcp_tool(self, tool_name: str, arguments: Dict) -> Dict:
        """Call an MCP tool using JSON-RPC 2.0."""
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        self.request_id += 1
        
        response = requests.post(self.mcp_endpoint, json=payload)
        response.raise_for_status()
        
        data = response.json()
        if data.get("error"):
            raise Exception(f"MCP Error: {data['error']['message']}")
        
        return data["result"]
    
    def discover_tools(self) -> Dict:
        """Discover available MCP tools."""
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list"
        }
        self.request_id += 1
        
        response = requests.post(self.mcp_endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def print_header(self, text: str):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.END}\n")
    
    def print_success(self, text: str):
        print(f"{Colors.GREEN}✅ {text}{Colors.END}")
    
    def print_step(self, step: int, text: str):
        print(f"\n{Colors.BLUE}{Colors.BOLD}Step {step}: {text}{Colors.END}")
    
    def print_info(self, text: str):
        print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")
    
    def run_demo(self):
        """Run the complete MCP demo flow."""
        self.print_header("NIKE ACP POC - MCP PROTOCOL DEMO")
        print(f"{Colors.BOLD}Demonstrating AI agent commerce using MCP tools{Colors.END}\n")
        
        # Step 0: Discover tools
        self.print_step(0, "Discover Available Tools (MCP)")
        tools_response = self.discover_tools()
        tools = tools_response["result"]["tools"]
        self.print_success(f"Discovered {len(tools)} commerce tools:")
        for tool in tools:
            print(f"   🔧 {tool['name']} - {tool['description'][:60]}...")
        
        # Step 1: Search products
        self.print_step(1, "Search Products (MCP Tool)")
        self.print_info("Calling tool: search_products(query='Air Max', limit=2)")
        
        search_result = self.call_mcp_tool('search_products', {
            'query': 'Air Max',
            'limit': 2
        })
        
        # Parse products from result
        products_text = search_result['content'][1]['resource']['text']
        products = eval(products_text)
        
        self.print_success(f"Found {len(products)} products:")
        for p in products:
            print(f"   👟 {p['title']} - ${p['price']} ({p['availability']})")
        
        # Step 2: Create checkout
        self.print_step(2, "Create Checkout Session (MCP Tool)")
        product_gtin = products[0]['gtin']
        self.print_info(f"Calling tool: create_checkout(items=[{{gtin: {product_gtin}, qty: 1}}])")
        
        checkout_result = self.call_mcp_tool('create_checkout', {
            'items': [{'gtin': product_gtin, 'quantity': 1}],
            'buyer_email': 'john.doe@example.com'
        })
        
        checkout_data = eval(checkout_result['content'][1]['resource']['text'])
        session_id = checkout_data['session_id']
        
        self.print_success(f"Checkout created: {session_id}")
        self.print_info(f"Subtotal: ${checkout_data['subtotal']}")
        self.print_info(f"Status: {checkout_data['status']}")
        
        # Step 3: Add shipping address
        self.print_step(3, "Add Shipping Address (MCP Tool)")
        address = {
            "name": "John Doe",
            "address_line_1": "3775 SW Morrison",
            "city": "Portland",
            "state": "OR",
            "postal_code": "97220",
            "country": "US"
        }
        self.print_info(f"Calling tool: add_shipping_address(address=Portland, OR)")
        
        shipping_result = self.call_mcp_tool('add_shipping_address', {
            'session_id': session_id,
            'address': address
        })
        
        shipping_data = eval(shipping_result['content'][1]['resource']['text'])
        
        self.print_success("Shipping calculated:")
        print(f"   📍 Ship to: {address['city']}, {address['state']}")
        print(f"   💰 Breakdown:")
        print(f"      Items:    ${shipping_data['totals']['items']}")
        print(f"      Shipping: ${shipping_data['totals']['shipping']}")
        print(f"      Tax:      ${shipping_data['totals']['tax']}")
        print(f"      ─────────────────")
        print(f"      Total:    ${shipping_data['totals']['total']}")
        
        # Step 4: Complete purchase
        self.print_step(4, "Complete Purchase (MCP Tool)")
        self.print_info("Calling tool: complete_purchase(payment_method=test card)")
        
        purchase_result = self.call_mcp_tool('complete_purchase', {
            'session_id': session_id,
            'payment_method': {
                'card_number': '4242424242424242',
                'exp_month': 12,
                'exp_year': 2025,
                'cvc': '123'
            }
        })
        
        order_data = eval(purchase_result['content'][1]['resource']['text'])
        
        if order_data.get('success'):
            self.print_success("🎉 Order confirmed!")
            print(f"   📦 Order ID: {order_data['order_id']}")
            print(f"   💵 Total: ${order_data['total']}")
            print(f"   🔗 Link: {order_data['permalink']}")
            print(f"   📧 {order_data['message']}")
        
        # Summary
        self.print_header("DEMO COMPLETE - MCP PROTOCOL")
        self.print_success("All commerce operations completed using MCP tools!")
        print(f"\n{Colors.BOLD}What this demonstrates:{Colors.END}")
        print(f"  ✅ AI agents can discover tools dynamically")
        print(f"  ✅ Complete purchase flow via tool invocation")
        print(f"  ✅ No hardcoded API knowledge required")
        print(f"  ✅ Works with ChatGPT, Claude, Gemini, etc.")
        print(f"\n{Colors.GREEN}{Colors.BOLD}MCP enables true agentic commerce! 🚀{Colors.END}\n")


if __name__ == "__main__":
    tester = MCPFlowTester()
    tester.run_demo()

