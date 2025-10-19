import { create } from 'zustand'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'
const MCP_ENDPOINT = `${API_BASE}/mcp`

// Helper function to call MCP tools
const callMCPTool = async (toolName, arguments) => {
  const response = await axios.post(MCP_ENDPOINT, {
    jsonrpc: "2.0",
    id: Date.now(),
    method: "tools/call",
    params: {
      name: toolName,
      arguments: arguments
    }
  })
  
  if (response.data.error) {
    throw new Error(response.data.error.message)
  }
  
  return response.data.result
}

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
  
  // Search products using MCP
  searchProducts: async (query) => {
    const startTime = Date.now()
    
    try {
      // Use MCP search_products tool
      const result = await callMCPTool('search_products', {
        query: query,
        limit: 1
      })
      
      get().logApiCall({
        method: 'MCP',
        endpoint: 'tools/call: search_products',
        status: 200,
        duration: Date.now() - startTime
      })
      
      // Parse product from MCP response
      const productsText = result.content.find(c => c.type === 'resource')?.resource?.text
      const products = productsText ? eval(productsText) : []
      
      if (products.length > 0) {
        const product = products[0]
        
        // Now create checkout with this product using MCP
        const checkoutStart = Date.now()
        const checkoutResult = await callMCPTool('create_checkout', {
          items: [{ gtin: product.gtin, quantity: 1 }],
          buyer_email: 'john.doe@example.com'
        })
        
        get().logApiCall({
          method: 'MCP',
          endpoint: 'tools/call: create_checkout',
          status: 200,
          duration: Date.now() - checkoutStart
        })
        
        // Parse session from response
        const sessionText = checkoutResult.content.find(c => c.type === 'resource')?.resource?.text
        const sessionData = sessionText ? eval(sessionText) : {}
        
        // Store session ID for later
        set({ currentSession: { id: sessionData.session_id, status: sessionData.status } })
        
        get().addMessage({
          role: 'assistant',
          content: "I found this Nike Air Max 90 for you:",
          products: [product]
        })
      }
      
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
  
  // Add shipping address using MCP
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
      
      // Use MCP add_shipping_address tool
      const result = await callMCPTool('add_shipping_address', {
        session_id: currentSession.id,
        address: shippingAddress
      })
      
      get().logApiCall({
        method: 'MCP',
        endpoint: 'tools/call: add_shipping_address',
        status: 200,
        duration: Date.now() - startTime
      })
      
      // Parse response
      const responseText = result.content.find(c => c.type === 'resource')?.resource?.text
      const sessionData = responseText ? eval(responseText) : {}
      
      // Build session object for UI
      const session = {
        id: sessionData.session_id,
        status: sessionData.status,
        fulfillment_address: sessionData.shipping_address,
        fulfillment_options: sessionData.shipping_options,
        selected_fulfillment_option_id: sessionData.selected_shipping,
        totals: {
          items_total: { value: sessionData.totals?.items || '0' },
          fulfillment: { value: sessionData.totals?.shipping || '0' },
          taxes: { value: sessionData.totals?.tax || '0' },
          total: { value: sessionData.totals?.total || '0' }
        },
        line_items: [{ title: "Nike Air Max 90", quantity: 1, total: sessionData.totals?.items || '0' }]
      }
      
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
  
  // Complete checkout using MCP
  completeCheckout: async (sessionId) => {
    const startTime = Date.now()
    
    try {
      // Use MCP complete_purchase tool
      const result = await callMCPTool('complete_purchase', {
        session_id: sessionId,
        payment_method: {
          card_number: "4242424242424242",
          exp_month: 12,
          exp_year: 2025,
          cvc: "123"
        }
      })
      
      get().logApiCall({
        method: 'MCP',
        endpoint: 'tools/call: complete_purchase',
        status: 200,
        duration: Date.now() - startTime
      })
      
      // Parse response
      const responseText = result.content.find(c => c.type === 'resource')?.resource?.text
      const orderData = responseText ? eval(responseText) : {}
      
      // Build order confirmation for UI
      const orderConfirmation = {
        id: sessionId,
        status: 'completed',
        order: {
          id: orderData.order_id,
          checkout_session_id: sessionId,
          permalink: orderData.permalink,
          created_at: new Date().toISOString()
        },
        messages: [
          {
            type: 'success',
            text: orderData.message || 'Your order has been confirmed!'
          }
        ]
      }
      
      get().addMessage({
        role: 'assistant',
        content: "🎉 Your order has been placed successfully!",
        orderConfirmation: orderConfirmation
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

