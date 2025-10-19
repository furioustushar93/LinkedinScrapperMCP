import { Trash2, Info, Github, Linkedin } from 'lucide-react'

function Sidebar({ onClearChat, isConnected }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo Section */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <Linkedin className="w-6 h-6 text-primary-600" />
          <span className="font-bold text-lg">Scraper AI</span>
        </div>
      </div>

      {/* Actions */}
      <div className="p-4 space-y-2">
        <button
          onClick={onClearChat}
          disabled={!isConnected}
          className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Trash2 className="w-5 h-5 text-gray-600" />
          <span className="text-sm font-medium text-gray-700">Clear Chat</span>
        </button>
      </div>

      {/* Info Section */}
      <div className="mt-auto p-4 border-t border-gray-200">
        <div className="space-y-4">
          <div className="flex items-start space-x-2 text-sm text-gray-600">
            <Info className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-medium mb-1">How to use:</p>
              <ul className="space-y-1 text-xs">
                <li>• Ask about LinkedIn jobs</li>
                <li>• Search for profiles</li>
                <li>• Get company info</li>
                <li>• Ask follow-up questions</li>
              </ul>
            </div>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-sm text-gray-600 hover:text-primary-600 transition-colors"
          >
            <Github className="w-4 h-4" />
            <span>View on GitHub</span>
          </a>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar

