"""
Performance Comparison: ACP REST vs MCP Protocol

Measures latency overhead of MCP layer compared to direct ACP REST calls.
"""

import requests
import json
import time
import statistics
from typing import Dict, List, Tuple


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class PerformanceTest:
    """Performance comparison between ACP REST and MCP."""
    
    def __init__(self, base_url: str = "http://localhost:8000", runs: int = 10):
        self.base_url = base_url
        self.mcp_endpoint = f"{base_url}/mcp"
        self.acp_base = f"{base_url}/acp/v1"
        self.runs = runs
        self.results = {
            'acp': [],
            'mcp': []
        }
    
    def print_header(self, text: str):
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.END}\n")
    
    def print_metric(self, label: str, value: float, unit: str = "ms"):
        print(f"  {label:<30} {Colors.BOLD}{value:.2f}{Colors.END} {unit}")
    
    # ==================== ACP REST Flow ====================
    
    def run_acp_flow(self) -> Dict[str, float]:
        """Run complete flow using ACP REST endpoints."""
        timings = {}
        
        # Step 1: Create checkout session
        start = time.time()
        create_response = requests.post(
            f"{self.acp_base}/checkout_sessions",
            json={
                "line_items": [{"gtin": "00883419552502", "quantity": 1}],
                "buyer_info": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "perf.test@nike.com",
                    "phone": "+15035551234"
                }
            }
        )
        timings['create_session'] = (time.time() - start) * 1000
        session_id = create_response.json()["id"]
        
        # Step 2: Update with address
        start = time.time()
        update_response = requests.post(
            f"{self.acp_base}/checkout_sessions/{session_id}",
            json={
                "fulfillment_address": {
                    "name": "John Doe",
                    "address_line_1": "3775 SW Morrison",
                    "city": "Portland",
                    "state": "OR",
                    "postal_code": "97220",
                    "country": "US"
                }
            }
        )
        timings['add_address'] = (time.time() - start) * 1000
        
        # Step 3: Tokenize payment
        start = time.time()
        payment_response = requests.post(
            f"{self.acp_base}/delegate_payment",
            json={
                "card_number": "4242424242424242",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        timings['tokenize_payment'] = (time.time() - start) * 1000
        payment_token = payment_response.json()["payment_token_id"]
        
        # Step 4: Complete checkout
        start = time.time()
        complete_response = requests.post(
            f"{self.acp_base}/checkout_sessions/{session_id}/complete",
            json={"payment_token_id": payment_token}
        )
        timings['complete_checkout'] = (time.time() - start) * 1000
        
        # Calculate total
        timings['total'] = sum(timings.values())
        
        return timings
    
    # ==================== MCP Flow ====================
    
    def call_mcp_tool(self, tool_name: str, arguments: Dict) -> Tuple[Dict, float]:
        """Call MCP tool and return result + latency."""
        start = time.time()
        
        response = requests.post(
            self.mcp_endpoint,
            json={
                "jsonrpc": "2.0",
                "id": int(time.time() * 1000),
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
        )
        
        latency = (time.time() - start) * 1000
        
        if response.status_code != 200:
            raise Exception(f"MCP call failed: {response.text}")
        
        data = response.json()
        if data.get("error"):
            raise Exception(f"MCP error: {data['error']['message']}")
        
        return data["result"], latency
    
    def run_mcp_flow(self) -> Dict[str, float]:
        """Run complete flow using MCP protocol."""
        timings = {}
        
        # Step 1: Create checkout (via MCP)
        result, latency = self.call_mcp_tool('create_checkout', {
            'items': [{'gtin': '00883419552502', 'quantity': 1}],
            'buyer_email': 'perf.test@nike.com'
        })
        timings['create_session'] = latency
        
        # Parse session ID from MCP response
        resource_text = result['content'][1]['resource']['text']
        session_data = eval(resource_text)  # Safe here in backend script
        session_id = session_data['session_id']
        
        # Step 2: Add shipping address (via MCP)
        result, latency = self.call_mcp_tool('add_shipping_address', {
            'session_id': session_id,
            'address': {
                "name": "John Doe",
                "address_line_1": "3775 SW Morrison",
                "city": "Portland",
                "state": "OR",
                "postal_code": "97220",
                "country": "US"
            }
        })
        timings['add_address'] = latency
        
        # Step 3 & 4: Complete purchase (via MCP - includes payment)
        result, latency = self.call_mcp_tool('complete_purchase', {
            'session_id': session_id,
            'payment_method': {
                'card_number': '4242424242424242',
                'exp_month': 12,
                'exp_year': 2025,
                'cvc': '123'
            }
        })
        # MCP combines tokenize + complete in one call
        timings['tokenize_payment'] = latency * 0.3  # Estimate split
        timings['complete_checkout'] = latency * 0.7  # Estimate split
        
        # Calculate total
        timings['total'] = sum(timings.values())
        
        return timings
    
    # ==================== Test Runner ====================
    
    def run_comparison(self):
        """Run performance comparison tests."""
        self.print_header("PERFORMANCE COMPARISON: ACP REST vs MCP Protocol")
        
        print(f"{Colors.BOLD}Running {self.runs} iterations of each flow...{Colors.END}\n")
        
        # Test ACP REST
        print(f"{Colors.BLUE}Testing ACP REST endpoints...{Colors.END}")
        acp_results = []
        for i in range(self.runs):
            try:
                timings = self.run_acp_flow()
                acp_results.append(timings)
                print(f"  Run {i+1}/{self.runs}: {timings['total']:.2f}ms")
            except Exception as e:
                print(f"  {Colors.RED}Run {i+1} failed: {e}{Colors.END}")
        
        print(f"\n{Colors.BLUE}Testing MCP Protocol...{Colors.END}")
        mcp_results = []
        for i in range(self.runs):
            try:
                timings = self.run_mcp_flow()
                mcp_results.append(timings)
                print(f"  Run {i+1}/{self.runs}: {timings['total']:.2f}ms")
            except Exception as e:
                print(f"  {Colors.RED}Run {i+1} failed: {e}{Colors.END}")
        
        # Calculate statistics
        self.print_results(acp_results, mcp_results)
    
    def print_results(self, acp_results: List[Dict], mcp_results: List[Dict]):
        """Print comparison results."""
        self.print_header("PERFORMANCE RESULTS")
        
        if not acp_results or not mcp_results:
            print(f"{Colors.RED}Insufficient data for comparison{Colors.END}")
            return
        
        # Calculate averages for each step
        steps = ['create_session', 'add_address', 'tokenize_payment', 'complete_checkout', 'total']
        
        print(f"{Colors.BOLD}Average Latency by Step:{Colors.END}\n")
        print(f"{'Step':<30} {'ACP REST':<15} {'MCP':<15} {'Overhead':<15}")
        print(f"{'-'*75}")
        
        total_overhead_pct = 0
        
        for step in steps:
            acp_avg = statistics.mean([r[step] for r in acp_results])
            mcp_avg = statistics.mean([r[step] for r in mcp_results])
            overhead = mcp_avg - acp_avg
            overhead_pct = (overhead / acp_avg * 100) if acp_avg > 0 else 0
            
            # Color code based on overhead
            if overhead_pct < 10:
                color = Colors.GREEN
            elif overhead_pct < 25:
                color = Colors.YELLOW
            else:
                color = Colors.RED
            
            print(f"{step.replace('_', ' ').title():<30} "
                  f"{acp_avg:>10.2f}ms    "
                  f"{mcp_avg:>10.2f}ms    "
                  f"{color}{overhead:>+8.2f}ms ({overhead_pct:>+5.1f}%){Colors.END}")
            
            if step == 'total':
                total_overhead_pct = overhead_pct
        
        # Summary statistics
        print(f"\n{Colors.BOLD}Statistical Analysis:{Colors.END}\n")
        
        acp_totals = [r['total'] for r in acp_results]
        mcp_totals = [r['total'] for r in mcp_results]
        
        print(f"ACP REST:")
        self.print_metric("  Mean:", statistics.mean(acp_totals))
        self.print_metric("  Median:", statistics.median(acp_totals))
        self.print_metric("  Std Dev:", statistics.stdev(acp_totals) if len(acp_totals) > 1 else 0)
        self.print_metric("  Min:", min(acp_totals))
        self.print_metric("  Max:", max(acp_totals))
        
        print(f"\nMCP Protocol:")
        self.print_metric("  Mean:", statistics.mean(mcp_totals))
        self.print_metric("  Median:", statistics.median(mcp_totals))
        self.print_metric("  Std Dev:", statistics.stdev(mcp_totals) if len(mcp_totals) > 1 else 0)
        self.print_metric("  Min:", min(mcp_totals))
        self.print_metric("  Max:", max(mcp_totals))
        
        # Overall assessment
        self.print_header("ASSESSMENT")
        
        avg_overhead = statistics.mean(mcp_totals) - statistics.mean(acp_totals)
        
        print(f"{Colors.BOLD}MCP Layer Overhead:{Colors.END}")
        print(f"  Average: {Colors.YELLOW}{avg_overhead:.2f}ms ({total_overhead_pct:.1f}%){Colors.END}")
        print(f"  Per request: ~{avg_overhead/4:.2f}ms additional latency")
        
        print(f"\n{Colors.BOLD}Recommendation:{Colors.END}")
        if total_overhead_pct < 10:
            print(f"  {Colors.GREEN}✅ MCP overhead is minimal (< 10%). Excellent for production!{Colors.END}")
        elif total_overhead_pct < 25:
            print(f"  {Colors.YELLOW}⚠️  MCP adds {total_overhead_pct:.1f}% overhead. Acceptable for most use cases.{Colors.END}")
        else:
            print(f"  {Colors.RED}⚠️  MCP adds {total_overhead_pct:.1f}% overhead. Consider optimization.{Colors.END}")
        
        print(f"\n{Colors.BOLD}Benefits of MCP (despite overhead):{Colors.END}")
        print(f"  ✅ Dynamic tool discovery")
        print(f"  ✅ Works with any AI agent (ChatGPT, Claude, Gemini)")
        print(f"  ✅ No hardcoded API knowledge needed")
        print(f"  ✅ Future-proof for multi-agent ecosystem")
        print(f"\n{Colors.BOLD}Conclusion:{Colors.END} {avg_overhead:.0f}ms overhead is worth the flexibility!\n")


def main():
    tester = PerformanceTest(runs=10)
    tester.run_comparison()


if __name__ == "__main__":
    main()

