import { Briefcase, Users, Building2, Sparkles } from 'lucide-react'

function WelcomeScreen({ onExampleClick }) {
  const examples = [
    {
      icon: Briefcase,
      title: "Search for Jobs",
      description: "Find AI engineer jobs in San Francisco",
      query: "Find AI engineer jobs in San Francisco"
    },
    {
      icon: Users,
      title: "Find Profiles",
      description: "Search for software engineers at Google",
      query: "Find profiles of software engineers at Google"
    },
    {
      icon: Building2,
      title: "Company Information",
      description: "Get information about Microsoft",
      query: "Tell me about Microsoft company"
    },
    {
      icon: Sparkles,
      title: "Ask Follow-ups",
      description: "Get details about specific results",
      query: "Tell me more about the first job"
    }
  ]

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)] space-y-8 animate-slide-up">
      {/* Welcome Message */}
      <div className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl shadow-lg">
          <Sparkles className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-4xl font-bold text-gray-900">
          Welcome to LinkedIn Scraper AI
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl">
          Your AI-powered assistant for LinkedIn job searches, profile lookups, and company research.
          Powered by Google Gemini and the Model Context Protocol.
        </p>
      </div>

      {/* Example Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-3xl mt-8">
        {examples.map((example, index) => {
          const Icon = example.icon
          return (
            <button
              key={index}
              onClick={() => onExampleClick(example.query)}
              className="card text-left hover:shadow-md hover:border-primary-200 transition-all duration-200 group"
            >
              <div className="flex items-start space-x-4">
                <div className="p-3 bg-primary-50 rounded-lg group-hover:bg-primary-100 transition-colors">
                  <Icon className="w-6 h-6 text-primary-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {example.title}
                  </h3>
                  <p className="text-sm text-gray-600">
                    {example.description}
                  </p>
                </div>
              </div>
            </button>
          )
        })}
      </div>

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl w-full mt-8">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Pro Tips:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Results are numbered - reference them in follow-up questions</li>
          <li>• Ask conversational questions about the results</li>
          <li>• Be specific about locations, titles, and requirements</li>
          <li>• Use natural language - no special syntax required</li>
        </ul>
      </div>
    </div>
  )
}

export default WelcomeScreen

