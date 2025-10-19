import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'
import DebugPanel from './components/DebugPanel'

function App() {
  const [showDebug, setShowDebug] = useState(false)

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      <Header onToggleDebug={() => setShowDebug(!showDebug)} showDebug={showDebug} />
      
      <div className="flex-1 flex overflow-hidden">
        <div className={showDebug ? "flex-1" : "w-full"}>
          <ChatInterface />
        </div>
        
        {showDebug && (
          <div className="w-96 border-l border-gray-700">
            <DebugPanel />
          </div>
        )}
      </div>
    </div>
  )
}

export default App

