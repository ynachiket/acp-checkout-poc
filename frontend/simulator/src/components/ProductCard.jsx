import { useStore } from '../store'

export default function ProductCard({ product }) {
  const { addToCart } = useStore()
  
  return (
    <div className="bg-gray-700 rounded-lg p-4 border border-gray-600">
      <div className="flex space-x-4">
        {/* Product Image */}
        <div className="w-24 h-24 bg-gray-600 rounded-lg flex items-center justify-center flex-shrink-0">
          {product.images && product.images[0] ? (
            <img 
              src={product.images[0]} 
              alt={product.title}
              className="w-full h-full object-cover rounded-lg"
              onError={(e) => {
                e.target.style.display = 'none'
                e.target.parentElement.innerHTML = '<span class="text-gray-400 text-4xl">👟</span>'
              }}
            />
          ) : (
            <span className="text-gray-400 text-4xl">👟</span>
          )}
        </div>
        
        {/* Product Details */}
        <div className="flex-1">
          <h3 className="font-semibold text-white mb-1">{product.title}</h3>
          <p className="text-gray-400 text-sm mb-2 line-clamp-2">{product.description}</p>
          
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xl font-bold text-white">${product.price}</span>
              <span className="text-gray-400 text-sm ml-2">{product.currency}</span>
            </div>
            
            <button
              onClick={() => addToCart(product)}
              className="px-4 py-2 bg-nike-orange hover:bg-orange-600 text-white rounded-lg font-medium transition-colors text-sm"
            >
              Add to Cart
            </button>
          </div>
          
          {product.availability === 'in_stock' && (
            <span className="inline-block mt-2 px-2 py-1 bg-green-900 text-green-300 text-xs rounded">
              ✓ In Stock
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

