export default function OrderConfirmation({ data }) {
  return (
    <div className="bg-gradient-to-br from-green-900 to-green-800 rounded-lg p-6 border-2 border-green-600">
      <div className="text-center mb-4">
        <div className="w-16 h-16 mx-auto mb-3 bg-green-600 rounded-full flex items-center justify-center">
          <span className="text-white text-3xl">✓</span>
        </div>
        <h3 className="text-2xl font-bold text-white mb-2">Order Confirmed!</h3>
        <p className="text-green-200">Your Nike order has been successfully placed</p>
      </div>
      
      <div className="bg-green-950 rounded-lg p-4 mb-4">
        <div className="flex justify-between mb-2">
          <span className="text-green-300 text-sm">Order Number:</span>
          <span className="text-white font-mono font-semibold">{data.order.id}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-green-300 text-sm">Order Date:</span>
          <span className="text-white text-sm">
            {new Date(data.order.created_at).toLocaleString()}
          </span>
        </div>
      </div>
      
      {data.messages && data.messages.map((msg, i) => (
        <div key={i} className="text-green-100 text-sm bg-green-950 rounded p-3 mb-3">
          📧 {msg.text}
        </div>
      ))}
      
      <a
        href={data.order.permalink}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full text-center py-3 bg-white hover:bg-gray-100 text-gray-900 rounded-lg font-semibold transition-colors"
      >
        View Order Details →
      </a>
    </div>
  )
}

