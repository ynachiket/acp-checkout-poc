import { useStore } from '../store'

export default function DebugPanel() {
  const { apiCalls, currentSession } = useStore()
  
  return (
    <div className="h-full flex flex-col bg-gray-800">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-white font-semibold">🔍 Debug Panel</h3>
        <p className="text-gray-400 text-xs mt-1">API calls and state</p>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Current Session */}
        {currentSession && (
          <div>
            <h4 className="text-sm font-semibold text-gray-300 mb-2">Current Session:</h4>
            <div className="bg-gray-900 rounded p-3 text-xs font-mono text-gray-400 overflow-x-auto">
              <div>ID: {currentSession.id}</div>
              <div>Status: <span className={
                currentSession.status === 'ready_for_payment' ? 'text-green-400' :
                currentSession.status === 'completed' ? 'text-blue-400' :
                'text-yellow-400'
              }>{currentSession.status}</span></div>
              {currentSession.totals && (
                <div>Total: ${currentSession.totals.total?.value}</div>
              )}
            </div>
          </div>
        )}
        
        {/* API Calls */}
        <div>
          <h4 className="text-sm font-semibold text-gray-300 mb-2">
            API Calls ({apiCalls.length}):
          </h4>
          <div className="space-y-2">
            {apiCalls.slice().reverse().map((call, i) => (
              <div key={i} className="bg-gray-900 rounded p-3 text-xs">
                <div className="flex items-center space-x-2 mb-2">
                  <span className={`px-2 py-1 rounded font-semibold ${
                    call.method === 'POST' ? 'bg-green-900 text-green-300' :
                    call.method === 'GET' ? 'bg-blue-900 text-blue-300' :
                    'bg-gray-700 text-gray-300'
                  }`}>
                    {call.method}
                  </span>
                  <span className="text-gray-400 font-mono truncate">
                    {call.endpoint}
                  </span>
                </div>
                
                {call.status && (
                  <div className={`text-xs ${
                    call.status >= 200 && call.status < 300 ? 'text-green-400' :
                    'text-red-400'
                  }`}>
                    Status: {call.status}
                  </div>
                )}
                
                {call.duration && (
                  <div className="text-gray-500 text-xs mt-1">
                    ⏱️ {call.duration}ms
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

