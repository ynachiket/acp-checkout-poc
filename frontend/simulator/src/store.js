import { create } from 'zustand'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

export const useStore = create((set, get) => ({
  messages: [],
  currentSession: null,
  cart: [],
  apiCalls: [],
  
  // Add message to chat
  addMessage: (message) => set((state) => ({ 
    messages: [...state.messages, message] 
  })),
  
  // Log API call
  logApiCall: (call) => set((state) => ({
    apiCalls: [...state.apiCalls, { ...call, timestamp: new Date() }]
  })),
  
  // Handle user message
  handleUserMessage: async (userMessage) => {
    const message = userMessage.toLowerCase()
    const { currentSession } = get()
    
    // Route based on intent and current state
    if (message.includes('buy') || message.includes('air max') || message.includes('nike') || message.includes('shoes')) {
      if (!currentSession) {
        await get().searchProducts('air max')
      } else if (currentSession.status === 'not_ready_for_payment') {
        // User responded after adding to cart
        await get().addShippingAddress(userMessage)
      }
    }
    else if (message.includes('cart') || message.includes('add')) {
      await get().addToCart()
    }
    else if (message.includes('ship') || message.includes('address') || message.includes('portland') || message.includes('york')) {
      await get().addShippingAddress(userMessage)
    }
    else if (message.includes('complete') || message.includes('checkout') || message.includes('pay') || message.includes('yes')) {
      await get().initiateCheckout()
    }
    else {
      // Check if waiting for shipping address
      if (currentSession && currentSession.status === 'not_ready_for_payment') {
        // User responded but we didn't catch it - assume it's shipping info
        await get().addShippingAddress(userMessage)
      } else {
        // Default response
        get().addMessage({
          role: 'assistant',
          content: "I can help you shop for Nike products! Try:\n• 'I want to buy Nike Air Max shoes'\n• 'Show me running shoes'\n• 'Add to cart'"
        })
      }
    }
  },
  
  // Search products
  searchProducts: async (query) => {
    const startTime = Date.now()
    
    try {
      // For demo, we'll use GTIN to get specific product
      const response = await axios.post(`${API_BASE}/acp/v1/checkout_sessions`, {
        line_items: [{ gtin: '00883419552502', quantity: 1 }],
        buyer_info: {
          first_name: "John",
          last_name: "Doe",
          email: "john.doe@example.com",
          phone: "+15035551234"
        }
      })
      
      get().logApiCall({
        method: 'POST',
        endpoint: '/acp/v1/checkout_sessions',
        status: response.status,
        duration: Date.now() - startTime
      })
      
      // Get product details from session
      const session = response.data
      const product = {
        gtin: session.line_items[0].gtin,
        title: session.line_items[0].title,
        price: session.line_items[0].unit_price,
        currency: 'USD',
        description: "Nothing as fly, nothing as comfortable. The Nike Air Max 90 stays true to its OG running roots.",
        availability: 'in_stock'
      }
      
      // Store session
      set({ currentSession: session })
      
      get().addMessage({
        role: 'assistant',
        content: "I found this Nike Air Max 90 for you:",
        products: [product]
      })
      
    } catch (error) {
      console.error('Search error:', error)
      get().addMessage({
        role: 'assistant',
        content: "Sorry, I encountered an error searching for products. Please make sure the backend server is running."
      })
    }
  },
  
  // Add to cart
  addToCart: async (product) => {
    const { currentSession } = get()
    
    if (currentSession) {
      get().addMessage({
        role: 'assistant',
        content: "Great! I've added the Nike Air Max 90 to your cart. Where would you like it shipped?"
      })
    } else {
      get().addMessage({
        role: 'assistant',
        content: "Please search for a product first!"
      })
    }
  },
  
  // Add shipping address
  addShippingAddress: async (message) => {
    const { currentSession } = get()
    
    if (!currentSession) {
      get().addMessage({
        role: 'assistant',
        content: "Please add items to your cart first!"
      })
      return
    }
    
    const startTime = Date.now()
    
    try {
      // Hardcoded shipping address for demo simplicity
      const shippingAddress = {
        name: "John Doe",
        address_line_1: "3775 SW Morrison",
        city: "Portland",
        state: "OR",
        postal_code: "97220",
        country: "US"
      }
      
      // Update session with address
      const response = await axios.post(
        `${API_BASE}/acp/v1/checkout_sessions/${currentSession.id}`,
        {
          fulfillment_address: shippingAddress
        }
      )
      
      get().logApiCall({
        method: 'POST',
        endpoint: `/acp/v1/checkout_sessions/${currentSession.id}`,
        status: response.status,
        duration: Date.now() - startTime
      })
      
      const session = response.data
      set({ currentSession: session })
      
      get().addMessage({
        role: 'assistant',
        content: "Perfect! I've calculated shipping and tax for your order:",
        checkoutSummary: session
      })
      
    } catch (error) {
      console.error('Address error:', error)
      get().addMessage({
        role: 'assistant',
        content: "Sorry, I had trouble processing that address. Please try again."
      })
    }
  },
  
  // Complete checkout
  completeCheckout: async (sessionId) => {
    const startTime = Date.now()
    
    try {
      // First, tokenize payment
      const paymentResponse = await axios.post(`${API_BASE}/acp/v1/delegate_payment`, {
        card_number: "4242424242424242",
        exp_month: 12,
        exp_year: 2025,
        cvc: "123"
      })
      
      const paymentToken = paymentResponse.data.payment_token_id
      
      get().logApiCall({
        method: 'POST',
        endpoint: '/acp/v1/delegate_payment',
        status: paymentResponse.status,
        duration: Date.now() - startTime
      })
      
      // Then complete checkout
      const completeStart = Date.now()
      const completeResponse = await axios.post(
        `${API_BASE}/acp/v1/checkout_sessions/${sessionId}/complete`,
        { payment_token_id: paymentToken }
      )
      
      get().logApiCall({
        method: 'POST',
        endpoint: `/acp/v1/checkout_sessions/${sessionId}/complete`,
        status: completeResponse.status,
        duration: Date.now() - completeStart
      })
      
      const result = completeResponse.data
      
      get().addMessage({
        role: 'assistant',
        content: "🎉 Your order has been placed successfully!",
        orderConfirmation: result
      })
      
      // Reset session
      set({ currentSession: null })
      
    } catch (error) {
      console.error('Checkout error:', error)
      get().addMessage({
        role: 'assistant',
        content: "Sorry, there was an issue completing your purchase. Please try again."
      })
    }
  },
  
  // Initialize checkout
  initiateCheckout: async () => {
    const { currentSession } = get()
    
    if (!currentSession) {
      get().addMessage({
        role: 'assistant',
        content: "Your cart is empty. Would you like to browse Nike products?"
      })
      return
    }
    
    if (currentSession.status === 'not_ready_for_payment') {
      get().addMessage({
        role: 'assistant',
        content: "I need your shipping address to calculate the total. Where should I ship your order?"
      })
    } else {
      get().addMessage({
        role: 'assistant',
        content: "I'll process your payment now using a test card (4242...).",
      })
      
      // Auto-complete for demo
      await get().completeCheckout(currentSession.id)
    }
  }
}))

