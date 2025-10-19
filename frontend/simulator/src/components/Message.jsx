import ProductCard from './ProductCard'
import CheckoutSummary from './CheckoutSummary'
import OrderConfirmation from './OrderConfirmation'

export default function Message({ message }) {
  const isUser = message.role === 'user'
  
  return (
    <div className="flex items-start space-x-3">
      {!isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-white text-sm font-semibold">C</span>
        </div>
      )}
      
      <div className={`flex-1 ${isUser ? 'flex justify-end' : ''}`}>
        <div className={`rounded-lg px-4 py-3 max-w-2xl ${
          isUser 
            ? 'bg-blue-600 text-white ml-12' 
            : 'bg-gray-800 text-gray-100'
        }`}>
          {/* Text content */}
          {message.content && (
            <div className="whitespace-pre-wrap">{message.content}</div>
          )}
          
          {/* Products */}
          {message.products && message.products.length > 0 && (
            <div className="mt-4 space-y-3">
              {message.products.map((product, i) => (
                <ProductCard key={i} product={product} />
              ))}
            </div>
          )}
          
          {/* Checkout Summary */}
          {message.checkoutSummary && (
            <div className="mt-4">
              <CheckoutSummary data={message.checkoutSummary} />
            </div>
          )}
          
          {/* Order Confirmation */}
          {message.orderConfirmation && (
            <div className="mt-4">
              <OrderConfirmation data={message.orderConfirmation} />
            </div>
          )}
        </div>
      </div>
      
      {isUser && (
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-white text-sm font-semibold">U</span>
        </div>
      )}
    </div>
  )
}

