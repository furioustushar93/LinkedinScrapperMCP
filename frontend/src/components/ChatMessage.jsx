import { User, Bot, AlertCircle, ExternalLink, MapPin, Calendar, Building2 } from 'lucide-react'

function ChatMessage({ message }) {
  const isUser = message.type === 'user'
  const isError = message.type === 'error'

  // Try to parse content if it's a string that looks like JSON
  let parsedContent = message.content
  if (typeof message.content === 'string') {
    try {
      // Check if it looks like JSON
      if (message.content.trim().startsWith('[') || message.content.trim().startsWith('{')) {
        parsedContent = JSON.parse(message.content)
      }
    } catch (e) {
      // Not JSON, keep as string
      parsedContent = message.content
    }
  }

  const renderContent = () => {
    // If it's an array of job/profile/company results
    if (Array.isArray(parsedContent)) {
      return (
        <div className="space-y-4">
          {parsedContent.map((item, index) => {
            // Job result
            if (item.job_id || item.title) {
              return (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-lg text-gray-900">{item.title}</h3>
                    {item.job_url && (
                      <a
                        href={item.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700"
                      >
                        <ExternalLink className="w-5 h-5" />
                      </a>
                    )}
                  </div>
                  
                  <div className="space-y-2 text-sm text-gray-600">
                    {item.company && (
                      <div className="flex items-center space-x-2">
                        <Building2 className="w-4 h-4" />
                        <span className="font-medium">{item.company}</span>
                      </div>
                    )}
                    {item.location && (
                      <div className="flex items-center space-x-2">
                        <MapPin className="w-4 h-4" />
                        <span>{item.location}</span>
                      </div>
                    )}
                    {item.posted_at && (
                      <div className="flex items-center space-x-2">
                        <Calendar className="w-4 h-4" />
                        <span>{item.posted_at}</span>
                      </div>
                    )}
                  </div>

                  {item.description && (
                    <p className="mt-3 text-sm text-gray-700 line-clamp-3">
                      {item.description}
                    </p>
                  )}
                </div>
              )
            }
            
            // Profile result
            if (item.profile_url || item.name) {
              return (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                      {item.headline && (
                        <p className="text-sm text-gray-600">{item.headline}</p>
                      )}
                    </div>
                    {item.profile_url && (
                      <a
                        href={item.profile_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700"
                      >
                        <ExternalLink className="w-5 h-5" />
                      </a>
                    )}
                  </div>
                  
                  {item.location && (
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <MapPin className="w-4 h-4" />
                      <span>{item.location}</span>
                    </div>
                  )}
                </div>
              )
            }
            
            // Company result
            if (item.company_url || item.company_name) {
              return (
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-lg text-gray-900">{item.company_name}</h3>
                    {item.company_url && (
                      <a
                        href={item.company_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-700"
                      >
                        <ExternalLink className="w-5 h-5" />
                      </a>
                    )}
                  </div>
                  
                  {item.industry && (
                    <p className="text-sm text-gray-600 mb-2">{item.industry}</p>
                  )}
                  
                  {item.description && (
                    <p className="text-sm text-gray-700">{item.description}</p>
                  )}
                </div>
              )
            }
            
            // Generic object
            return (
              <pre key={index} className="text-sm bg-gray-50 p-3 rounded overflow-x-auto">
                {JSON.stringify(item, null, 2)}
              </pre>
            )
          })}
        </div>
      )
    }

    // Regular text content
    return (
      <div className="prose prose-sm max-w-none">
        <p className="whitespace-pre-wrap">{parsedContent}</p>
      </div>
    )
  }

  return (
    <div className={`flex space-x-3 mb-6 ${isUser ? 'flex-row-reverse space-x-reverse' : ''} animate-slide-up`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
        isError ? 'bg-red-100' : isUser ? 'bg-primary-100' : 'bg-gray-100'
      }`}>
        {isError ? (
          <AlertCircle className="w-6 h-6 text-red-600" />
        ) : isUser ? (
          <User className="w-6 h-6 text-primary-600" />
        ) : (
          <Bot className="w-6 h-6 text-gray-600" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-3xl ${isUser ? 'text-right' : ''}`}>
        <div className={`inline-block text-left ${
          isError ? 'bg-red-50 border border-red-200' :
          isUser ? 'bg-primary-50 border border-primary-200' : 
          'bg-white border border-gray-200'
        } rounded-lg px-4 py-3 shadow-sm`}>
          {renderContent()}
        </div>
        
        {/* Timestamp */}
        <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : ''}`}>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage

