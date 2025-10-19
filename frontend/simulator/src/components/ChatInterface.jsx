import { useState, useRef, useEffect } from 'react'
import { useStore } from '../store'
import Message from './Message'
import ProductCard from './ProductCard'
import CheckoutSummary from './CheckoutSummary'
import OrderConfirmation from './OrderConfirmation'

export default function ChatInterface() {
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  
  const { messages, addMessage, handleUserMessage } = useStore()
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isTyping) return
    
    const userMessage = input.trim()
    setInput('')
    
    // Add user message
    addMessage({ role: 'user', content: userMessage })
    setIsTyping(true)
    
    // Simulate typing delay
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Handle message and get response
    await handleUserMessage(userMessage)
    
    setIsTyping(false)
  }
  
  const quickActions = [
    "I want to buy Nike Air Max shoes",
    "Show me running shoes under $150",
    "Add size 10 to my cart",
    "Ship to 123 Main St, New York, NY 10001",
  ]
  
  return (
    <div className="flex flex-col h-full bg-gray-900">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-2xl">🛍️</span>
              </div>
              <h2 className="text-2xl font-semibold text-white mb-2">
                Nike Shopping Assistant
              </h2>
              <p className="text-gray-400 mb-6">
                I can help you find and purchase Nike products. Try asking:
              </p>
              <div className="grid grid-cols-2 gap-3 max-w-2xl mx-auto">
                {quickActions.map((action, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(action)}
                    className="px-4 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-sm text-left transition-colors border border-gray-700"
                  >
                    "{action}"
                  </button>
                ))}
              </div>
            </div>
          )}
          
          {messages.map((message, index) => (
            <Message key={index} message={message} />
          ))}
          
          {isTyping && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-white text-sm">C</span>
              </div>
              <div className="flex-1 bg-gray-800 rounded-lg px-4 py-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {/* Input Area */}
      <div className="border-t border-gray-700 bg-gray-800 px-4 py-4">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message ChatGPT..."
              disabled={isTyping}
              className="flex-1 bg-gray-700 text-white placeholder-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

