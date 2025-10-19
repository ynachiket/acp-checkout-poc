export default function Header({ onToggleDebug, showDebug }) {
  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="w-10 h-10 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">C</span>
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">ChatGPT Simulator</h1>
            <p className="text-gray-400 text-sm">Nike Agentic Commerce Demo</p>
          </div>
        </div>
        
        <button
          onClick={onToggleDebug}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            showDebug 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          {showDebug ? '🔍 Hide Debug' : '🔍 Show Debug'}
        </button>
      </div>
    </header>
  )
}

