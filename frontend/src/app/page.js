"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch("http://10.115.69.24:80/query/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query }),
      });

      if (!res.ok) {
        throw new Error(`Error: ${res.status}`);
      }

      const data = await res.json();
      setConversations(prev => [...prev, { question: query, response: data }]);
      setQuery("");
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(`Failed to get response: ${err.message}. Please check if the backend server is running on port 80.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? "bg-black text-white" : "bg-white text-black"}`}>
      {/* Dark Mode Toggle Button */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="fixed top-4 left-4 p-2 bg-gray-800 text-white rounded-lg shadow-md hover:bg-gray-700 transition"
      >
        {darkMode ? "Light Mode 🌞" : "Dark Mode 🌙"}
      </button>

      <div className="flex flex-col items-center justify-center min-h-screen">
        {conversations.length === 0 ? (
          <div className="w-full max-w-2xl px-4">
            <h1 className="text-3xl font-bold text-center mb-8">
              What can I help you with about Graceland?
            </h1>
            
            {/* Form Container */}
            <div className={`p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-900" : "bg-gray-100"}`}>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your question"
                  className={`w-full p-4 rounded-lg border ${
                    darkMode 
                      ? "bg-gray-800 text-white border-gray-700" 
                      : "bg-white text-black border-gray-300"
                  }`}
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg transition-colors"
                  disabled={isLoading}
                >
                  {isLoading ? "Loading..." : "Ask Question"}
                </button>
              </form>
              {error && <div className="text-red-500 mt-4">{error}</div>}
            </div>
          </div>
        ) : (
          <div className="w-full max-w-2xl px-4 py-8">
            {conversations.map((conv, index) => (
              <div key={index} className={`mb-6 p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-900" : "bg-gray-100"}`}>
                <div className="mb-4">
                  <h3 className="font-semibold">Question:</h3>
                  <p className="ml-4">{conv.question}</p>
                </div>
                
                <div>
                  <h3 className="font-semibold">Answer:</h3>
                  <p className="ml-4 mb-4">{conv.response.answer}</p>

                  {conv.response.sources && (
                    <>
                      <h4 className="font-semibold">Sources:</h4>
                      <div className={`p-3 rounded mt-2 ${darkMode ? "bg-gray-800" : "bg-gray-100"}`}>
                        <ul className="list-disc pl-5 space-y-2">
                          {conv.response.sources.map((source, idx) => (
                            <li key={idx} className="text-sm">
                              {source.source && source.source !== "None" ? (
                                <a 
                                  href={source.source} 
                                  target="_blank" 
                                  rel="noopener noreferrer" 
                                  className={`font-medium hover:underline ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}
                                >
                                  {source.title || "Unknown Title"}
                                </a>
                              ) : (
                                <span className="font-medium">
                                  {source.title || "Unknown Title"}
                                </span>
                              )}
                              {source.page && (
                                <span className="ml-2 text-gray-500">
                                  {darkMode ? "📄" : "📝"} Page {source.page}
                                </span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </>
                  )}
                </div>
              </div>
            ))}

            {/* Input for next question */}
            <div className={`p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-900" : "bg-gray-100"}`}>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask another question"
                  className={`w-full p-4 rounded-lg border ${
                    darkMode 
                      ? "bg-gray-800 text-white border-gray-700" 
                      : "bg-white text-black border-gray-300"
                  }`}
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg transition-colors"
                  disabled={isLoading}
                >
                  {isLoading ? "Loading..." : "Ask Question"}
                </button>
              </form>
              {error && <div className="text-red-500 mt-4">{error}</div>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
