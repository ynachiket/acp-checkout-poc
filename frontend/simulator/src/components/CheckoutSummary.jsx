import { useStore } from '../store'

export default function CheckoutSummary({ data }) {
  const { completeCheckout } = useStore()
  
  const totals = data.totals || {}
  const isReady = data.status === 'ready_for_payment'
  
  return (
    <div className="bg-gray-700 rounded-lg p-6 border border-gray-600">
      <h3 className="text-xl font-bold text-white mb-4">🛒 Checkout Summary</h3>
      
      {/* Items */}
      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-300 mb-2">Items:</h4>
        {data.line_items && data.line_items.map((item, i) => (
          <div key={i} className="flex justify-between text-sm mb-1">
            <span className="text-gray-300">
              {item.title} (×{item.quantity})
            </span>
            <span className="text-white font-medium">${item.total}</span>
          </div>
        ))}
      </div>
      
      {/* Shipping */}
      {data.fulfillment_address && (
        <div className="mb-4 pb-4 border-b border-gray-600">
          <h4 className="text-sm font-semibold text-gray-300 mb-2">📍 Shipping To:</h4>
          <p className="text-gray-400 text-sm">
            {data.fulfillment_address.name}<br />
            {data.fulfillment_address.address_line_1}<br />
            {data.fulfillment_address.city}, {data.fulfillment_address.state} {data.fulfillment_address.postal_code}
          </p>
        </div>
      )}
      
      {/* Shipping Options */}
      {data.fulfillment_options && (
        <div className="mb-4 pb-4 border-b border-gray-600">
          <h4 className="text-sm font-semibold text-gray-300 mb-2">🚚 Shipping:</h4>
          {data.fulfillment_options.map((option) => (
            <div 
              key={option.id}
              className={`text-sm p-2 rounded ${
                option.id === data.selected_fulfillment_option_id
                  ? 'bg-green-900 border border-green-700'
                  : 'bg-gray-800'
              }`}
            >
              <div className="flex justify-between">
                <span className="text-gray-300">
                  {option.id === data.selected_fulfillment_option_id && '✓ '}
                  {option.title}
                </span>
                <span className="text-white">${option.cost}</span>
              </div>
              <span className="text-gray-500 text-xs">{option.subtitle}</span>
            </div>
          ))}
        </div>
      )}
      
      {/* Totals */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Subtotal:</span>
          <span className="text-gray-300">${totals.subtotal?.value || '0.00'}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Shipping:</span>
          <span className="text-gray-300">${totals.fulfillment?.value || '0.00'}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Tax:</span>
          <span className="text-gray-300">${totals.taxes?.value || '0.00'}</span>
        </div>
        <div className="border-t border-gray-600 pt-2 mt-2"></div>
        <div className="flex justify-between text-lg font-bold">
          <span className="text-white">Total:</span>
          <span className="text-white">${totals.total?.value || '0.00'}</span>
        </div>
      </div>
      
      {/* Action Button */}
      {isReady && (
        <button
          onClick={() => completeCheckout(data.id)}
          className="w-full py-3 bg-nike-orange hover:bg-orange-600 text-white rounded-lg font-semibold transition-colors"
        >
          Complete Purchase
        </button>
      )}
      
      {!isReady && (
        <div className="text-center py-2 text-yellow-500 text-sm">
          ⚠️ Add shipping address to continue
        </div>
      )}
      
      <p className="text-xs text-gray-500 mt-3 text-center">
        Session ID: {data.id}
      </p>
    </div>
  )
}

