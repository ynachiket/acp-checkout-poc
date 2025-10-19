"""
ACP Client for MCP Handlers

MCP handlers use this client to delegate to ACP REST endpoints.
This implements the hybrid strategy: MCP discovery + ACP execution.
"""

import httpx
from typing import Dict, Any
from app.config import settings


class ACPClient:
    """
    Client for calling ACP REST endpoints from MCP handlers.
    
    This enables the hybrid strategy:
    - AI agents discover tools via MCP
    - Execution happens via scalable ACP REST endpoints
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or f"http://{settings.host}:{settings.port}/acp/v1"
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def create_checkout_session(self, line_items: list, buyer_info: Dict = None, fulfillment_address: Dict = None) -> Dict:
        """
        Call ACP create checkout session endpoint.
        
        Args:
            line_items: List of {gtin, quantity}
            buyer_info: Optional buyer information
            fulfillment_address: Optional shipping address
            
        Returns:
            ACP checkout session response
        """
        payload = {
            "line_items": line_items
        }
        
        if buyer_info:
            payload["buyer_info"] = buyer_info
        
        if fulfillment_address:
            payload["fulfillment_address"] = fulfillment_address
        
        response = await self.client.post(
            f"{self.base_url}/checkout_sessions",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def update_checkout_session(self, session_id: str, fulfillment_address: Dict = None, selected_fulfillment_option_id: str = None) -> Dict:
        """
        Call ACP update checkout session endpoint.
        
        Args:
            session_id: Checkout session ID
            fulfillment_address: Optional shipping address
            selected_fulfillment_option_id: Optional shipping option
            
        Returns:
            Updated ACP checkout session
        """
        payload = {}
        
        if fulfillment_address:
            payload["fulfillment_address"] = fulfillment_address
        
        if selected_fulfillment_option_id:
            payload["selected_fulfillment_option_id"] = selected_fulfillment_option_id
        
        response = await self.client.post(
            f"{self.base_url}/checkout_sessions/{session_id}",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    async def get_checkout_session(self, session_id: str) -> Dict:
        """
        Get checkout session.
        
        Args:
            session_id: Checkout session ID
            
        Returns:
            ACP checkout session
        """
        response = await self.client.get(
            f"{self.base_url}/checkout_sessions/{session_id}"
        )
        response.raise_for_status()
        return response.json()
    
    async def delegate_payment(self, card_details: Dict) -> str:
        """
        Tokenize payment via ACP delegate payment endpoint.
        
        Args:
            card_details: Payment method details
            
        Returns:
            Payment token ID
        """
        response = await self.client.post(
            f"{self.base_url}/delegate_payment",
            json=card_details
        )
        response.raise_for_status()
        return response.json()["payment_token_id"]
    
    async def complete_checkout_session(self, session_id: str, payment_token_id: str) -> Dict:
        """
        Complete checkout via ACP endpoint.
        
        Args:
            session_id: Checkout session ID
            payment_token_id: Payment token from delegate_payment
            
        Returns:
            Completed checkout with order details
        """
        response = await self.client.post(
            f"{self.base_url}/checkout_sessions/{session_id}/complete",
            json={"payment_token_id": payment_token_id}
        )
        response.raise_for_status()
        return response.json()
    
    async def cancel_checkout_session(self, session_id: str) -> Dict:
        """
        Cancel checkout session.
        
        Args:
            session_id: Checkout session ID
            
        Returns:
            Canceled session
        """
        response = await self.client.post(
            f"{self.base_url}/checkout_sessions/{session_id}/cancel"
        )
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

