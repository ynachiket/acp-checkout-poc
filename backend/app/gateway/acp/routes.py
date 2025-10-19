"""
ACP Protocol REST Endpoints

Implements the 5 required ACP endpoints.
TODO: Add comprehensive tests
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database import get_db
from app.services.checkout_service import CheckoutService
from app.services.payment_service import PaymentService
from app.services.order_service import OrderService

router = APIRouter(prefix="/acp/v1", tags=["ACP Protocol"])


@router.post("/checkout_sessions")
async def create_checkout_session(
    request: Dict,
    db: Session = Depends(get_db)
):
    """
    Create a new checkout session.
    
    ACP Endpoint: POST /checkout_sessions
    """
    try:
        checkout_service = CheckoutService(db)
        
        # Extract items from line_items
        items = []
        for item in request.get("line_items", []):
            # Convert GTIN to product_id (for POC, we'll search by GTIN)
            from app.services.product_service import ProductService
            product_service = ProductService(db)
            product = product_service.get_by_gtin(item["gtin"])
            
            items.append({
                "product_id": product.id,
                "quantity": item["quantity"]
            })
        
        # Create session
        session = checkout_service.create_session(
            items=items,
            address=request.get("fulfillment_address"),
            buyer_info=request.get("buyer_info")
        )
        
        # Convert to ACP format
        return {
            "id": session.id,
            "status": session.status,
            "currency": session.currency,
            "line_items": session.line_items,
            "fulfillment_address": session.fulfillment_address,
            "fulfillment_options": session.fulfillment_options,
            "selected_fulfillment_option_id": session.selected_fulfillment_option_id,
            "totals": session.totals,
            "buyer_info": session.buyer_info,
            "links": {
                "terms_of_service": "https://www.nike.com/us/terms",
                "privacy_policy": "https://www.nike.com/us/privacy"
            },
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "invalid", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(e)})


@router.post("/checkout_sessions/{session_id}")
async def update_checkout_session(
    session_id: str,
    request: Dict,
    db: Session = Depends(get_db)
):
    """
    Update an existing checkout session.
    
    ACP Endpoint: POST /checkout_sessions/{id}
    """
    try:
        checkout_service = CheckoutService(db)
        
        session = checkout_service.update_session(
            session_id=session_id,
            address=request.get("fulfillment_address"),
            fulfillment_option_id=request.get("selected_fulfillment_option_id")
        )
        
        return {
            "id": session.id,
            "status": session.status,
            "currency": session.currency,
            "line_items": session.line_items,
            "fulfillment_address": session.fulfillment_address,
            "fulfillment_options": session.fulfillment_options,
            "selected_fulfillment_option_id": session.selected_fulfillment_option_id,
            "totals": session.totals,
            "buyer_info": session.buyer_info,
            "links": {
                "terms_of_service": "https://www.nike.com/us/terms",
                "privacy_policy": "https://www.nike.com/us/privacy"
            },
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "invalid", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(e)})


@router.get("/checkout_sessions/{session_id}")
async def get_checkout_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a checkout session.
    
    ACP Endpoint: GET /checkout_sessions/{id}
    """
    try:
        checkout_service = CheckoutService(db)
        session = checkout_service.get_session(session_id)
        
        return {
            "id": session.id,
            "status": session.status,
            "currency": session.currency,
            "line_items": session.line_items,
            "fulfillment_address": session.fulfillment_address,
            "fulfillment_options": session.fulfillment_options,
            "selected_fulfillment_option_id": session.selected_fulfillment_option_id,
            "totals": session.totals,
            "buyer_info": session.buyer_info,
            "payment_token_id": session.payment_token_id,
            "order_id": session.order_id,
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": "missing", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(e)})


@router.post("/checkout_sessions/{session_id}/complete")
async def complete_checkout_session(
    session_id: str,
    request: Dict,
    db: Session = Depends(get_db)
):
    """
    Complete checkout and create order.
    
    ACP Endpoint: POST /checkout_sessions/{id}/complete
    """
    try:
        checkout_service = CheckoutService(db)
        payment_service = PaymentService()
        order_service = OrderService(db)
        
        # Get session
        session = checkout_service.get_session(session_id)
        
        # Verify session is ready
        if session.status != "ready_for_payment":
            raise ValueError("Session is not ready for payment")
        
        # Get payment token from request
        payment_token = request.get("payment_token_id")
        if not payment_token:
            raise ValueError("Payment token is required")
        
        # Process payment
        from decimal import Decimal
        total_amount = Decimal(session.totals["total"]["value"])
        payment_intent = payment_service.create_payment_intent(total_amount, payment_token)
        
        if payment_intent["status"] != "succeeded":
            raise ValueError("Payment failed")
        
        # Create order
        order = order_service.create_order(session, payment_intent["id"])
        
        # Update session
        session.status = "completed"
        session.payment_token_id = payment_token
        session.order_id = order.id
        db.commit()
        
        return {
            "id": session.id,
            "status": "completed",
            "order": {
                "id": order.id,
                "checkout_session_id": session.id,
                "permalink": order.permalink,
                "created_at": order.created_at.isoformat() if order.created_at else None
            },
            "messages": [
                {
                    "type": "success",
                    "text": f"Your order has been confirmed! You'll receive a confirmation email at {session.buyer_info.get('email', '')}"
                }
            ]
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"code": "payment_declined", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(e)})


@router.post("/checkout_sessions/{session_id}/cancel")
async def cancel_checkout_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Cancel a checkout session.
    
    ACP Endpoint: POST /checkout_sessions/{id}/cancel
    """
    try:
        checkout_service = CheckoutService(db)
        session = checkout_service.get_session(session_id)
        
        session.status = "canceled"
        db.commit()
        
        return {
            "id": session.id,
            "status": "canceled",
            "updated_at": session.updated_at.isoformat() if session.updated_at else None
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail={"code": "missing", "message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"code": "internal_error", "message": str(e)})


@router.post("/delegate_payment")
async def delegate_payment(request: Dict):
    """
    Tokenize payment information.
    
    ACP Endpoint: POST /delegate_payment
    """
    try:
        payment_service = PaymentService()
        
        # Extract card details from request
        card_details = {
            "card_number": request.get("card_number"),
            "exp_month": request.get("exp_month"),
            "exp_year": request.get("exp_year"),
            "cvc": request.get("cvc"),
            "billing_address": request.get("billing_address")
        }
        
        # Tokenize payment
        payment_token = payment_service.tokenize_payment(card_details)
        
        return {
            "payment_token_id": payment_token
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail={"code": "invalid", "message": str(e)})

