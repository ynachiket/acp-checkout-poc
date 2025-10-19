#!/bin/bash

# Nike ACP POC - API Demo Script
# 
# This script demonstrates the complete purchase flow using curl commands.
# Each step is clearly shown with colored output.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

BASE_URL=${1:-http://localhost:8000}

print_header() {
    echo -e "\n${BLUE}${BOLD}================================================${NC}"
    echo -e "${BLUE}${BOLD}$1${NC}"
    echo -e "${BLUE}${BOLD}================================================${NC}\n"
}

print_step() {
    echo -e "${GREEN}${BOLD}Step $1: $2${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if server is running
print_header "NIKE ACP POC - API DEMO"

print_step 0 "Health Check"
response=$(curl -s "$BASE_URL/health")
if [ $? -eq 0 ]; then
    print_success "API is healthy"
    echo "$response" | jq '.'
else
    print_error "API is not responding. Make sure the server is running:"
    echo "    uvicorn app.main:app --reload"
    exit 1
fi

# Step 1: Create checkout session
print_step 1 "Create Checkout Session"
print_info "Adding Nike Air Max 90 to cart with shipping address..."

SESSION_RESPONSE=$(curl -s -X POST "$BASE_URL/acp/v1/checkout_sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "line_items": [
      {
        "gtin": "00883419552502",
        "quantity": 1
      }
    ],
    "fulfillment_address": {
      "name": "John Doe",
      "address_line_1": "123 Main St",
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
  }')

SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.id')
TOTAL=$(echo "$SESSION_RESPONSE" | jq -r '.totals.total.value')

print_success "Session created: $SESSION_ID"
print_info "Total: \$$TOTAL"
echo ""
echo "$SESSION_RESPONSE" | jq '{id, status, line_items, totals}'

# Step 2: Get session
print_step 2 "Retrieve Checkout Session"
print_info "Fetching session details..."

GET_RESPONSE=$(curl -s "$BASE_URL/acp/v1/checkout_sessions/$SESSION_ID")
print_success "Session retrieved"
echo "$GET_RESPONSE" | jq '{id, status, totals}'

# Step 3: Tokenize payment
print_step 3 "Tokenize Payment"
print_info "Tokenizing test card: 4242 4242 4242 4242..."

PAYMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/acp/v1/delegate_payment" \
  -H "Content-Type: application/json" \
  -d '{
    "card_number": "4242424242424242",
    "exp_month": 12,
    "exp_year": 2025,
    "cvc": "123"
  }')

PAYMENT_TOKEN=$(echo "$PAYMENT_RESPONSE" | jq -r '.payment_token_id')
print_success "Payment tokenized: $PAYMENT_TOKEN"

# Step 4: Complete purchase
print_step 4 "Complete Purchase"
print_info "Processing payment and creating order..."

COMPLETE_RESPONSE=$(curl -s -X POST "$BASE_URL/acp/v1/checkout_sessions/$SESSION_ID/complete" \
  -H "Content-Type: application/json" \
  -d "{
    \"payment_token_id\": \"$PAYMENT_TOKEN\"
  }")

ORDER_ID=$(echo "$COMPLETE_RESPONSE" | jq -r '.order.id')

if [ "$ORDER_ID" != "null" ]; then
    print_success "🎉 Purchase completed successfully!"
    print_success "Order ID: $ORDER_ID"
    echo ""
    echo "$COMPLETE_RESPONSE" | jq '{id, status, order}'
else
    print_error "Purchase failed"
    echo "$COMPLETE_RESPONSE" | jq '.'
    exit 1
fi

# Summary
print_header "DEMO COMPLETE"
echo -e "${GREEN}${BOLD}✅ All steps completed successfully!${NC}\n"
echo -e "${BOLD}Summary:${NC}"
echo -e "  Session ID: $SESSION_ID"
echo -e "  Order ID: $ORDER_ID"
echo -e "  Total: \$$TOTAL"
echo ""
echo -e "${YELLOW}View API docs: $BASE_URL/docs${NC}\n"

