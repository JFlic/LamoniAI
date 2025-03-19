"use client";

import { useState } from "react";
import ReactMarkdown from 'react-markdown';

export default function Home() {
  const [query, setQuery] = useState("");
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  // Common questions for quick access
  const commonQuestions = [
    "Where/How do I join a campus club?",
    "What are popular campus events?",
    "I'm a new student, what do I need?",
    "Where do I eat on campus?"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
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
      
      // Process the sources to remove duplicates
      if (data.sources && data.sources.length > 0) {
        // Create a map to store unique sources based on their title and source URL
        const uniqueSourcesMap = new Map();
        
        data.sources.forEach(source => {
          const key = `${source.title || "Unknown"}|${source.source || "None"}`;
          
          // If this source hasn't been seen yet, or if the current source has a page number and the existing one doesn't
          if (!uniqueSourcesMap.has(key) || 
              (source.page && (!uniqueSourcesMap.get(key).page || uniqueSourcesMap.get(key).page > source.page))) {
            uniqueSourcesMap.set(key, source);
          }
        });
        
        // Convert the map values back to an array
        data.sources = Array.from(uniqueSourcesMap.values());
      }
      
      setConversations(prev => [...prev, { question: query, response: data }]);
      setQuery("");
    } catch (err) {
      console.error("Error fetching data:", err);
      setError(`Failed to get response: ${err.message}. Please check if the backend server is running on port 80.`);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle clicking a common question button
  const handleQuestionClick = (question) => {
    setQuery(question);
  };

  return (
    <div className={`min-h-screen ${darkMode ? "bg-gray-900 text-white" : "bg-white text-black"}`}>
      {/* Dark Mode Toggle Button */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className={`fixed top-4 left-4 p-2 rounded-lg shadow-md transition ${
          darkMode 
            ? "bg-gray-700 text-white hover:bg-gray-600" 
            : "bg-gray-200 text-black hover:bg-gray-300"
        }`}
      >
        {darkMode ? "Light Mode 🌞" : "Dark Mode 🌙"}
      </button>

      <div className="flex flex-col items-center justify-center min-h-screen">
        {conversations.length === 0 ? (
          <div className="w-full max-w-2xl px-4">
            <h1 className="text-3xl font-bold text-center mb-8">
              What can I help you with about our University?
            </h1>
            
            {/* Common Questions */}
            <div className={`mb-6 grid grid-cols-1 md:grid-cols-2 gap-3`}>
              {commonQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleQuestionClick(question)}
                  className={`p-3 rounded-lg text-left transition-colors ${
                    darkMode 
                      ? "bg-[#2757a3] hover:bg-[#1e437d] text-gray" 
                      : "bg-[#fbcc0d] hover:bg-[#eabd0c] text-black"
                  }`}
                >
                  {question}
                </button>
              ))}
            </div>
            
            {/* Form Container */}
            <div className={`p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-800" : "bg-gray-100"}`}>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your question"
                  className={`w-full p-4 rounded-lg border ${
                    darkMode 
                      ? "bg-gray-700 text-white border-gray-600" 
                      : "bg-white text-black border-gray-300"
                  }`}
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  className={`w-full p-4 rounded-lg transition-colors text-white ${
                    darkMode
                      ? "bg-[#0a3683] hover:bg-[#0b4094]"
                      : "bg-[#04215a] hover:bg-[#03184a]"
                  }`}
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
              <div key={index} className={`mb-6 p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-800" : "bg-gray-100"}`}>
                <div className="mb-4">
                  <h3 className="font-semibold">Question:</h3>
                  <p className="ml-4">{conv.question}</p>
                </div>
                
                <div>
                  <h3 className="font-semibold">Answer:</h3>
                  <div className="ml-4 mb-4 prose max-w-none">
                    <div className={darkMode ? "markdown-dark" : "markdown-light"}>
                      <ReactMarkdown>{conv.response.answer}</ReactMarkdown>
                    </div>
                  </div>

                  {conv.response.sources && conv.response.sources.length > 0 && (
                    <>
                      <h4 className="font-semibold">Sources:</h4>
                      <div className={`p-3 rounded mt-2 ${darkMode ? "bg-gray-700" : "bg-gray-200"}`}>
                        <ul className="list-disc pl-5 space-y-2">
                          {conv.response.sources.map((source, idx) => (
                            <li key={idx} className="text-sm">
                              {source.source && source.source !== "None" ? (
                                <a 
                                  href={source.source} 
                                  target="_blank" 
                                  rel="noopener noreferrer" 
                                  className={`font-medium hover:underline ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}
                                >
                                  {source.title || "Unknown Title"}
                                </a>
                              ) : (
                                <span className="font-medium">
                                  {source.title || "Unknown Title"}
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
            <div className={`p-6 rounded-lg shadow-lg ${darkMode ? "bg-gray-800" : "bg-gray-100"}`}>
              <form onSubmit={handleSubmit} className="space-y-4">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask another question"
                  className={`w-full p-4 rounded-lg border ${
                    darkMode 
                      ? "bg-gray-700 text-white border-gray-600" 
                      : "bg-white text-black border-gray-300"
                  }`}
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  className={`w-full p-4 rounded-lg transition-colors text-white ${
                    darkMode
                      ? "bg-[#0a3683] hover:bg-[#0b4094]"
                      : "bg-[#04215a] hover:bg-[#03184a]"
                  }`}
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
      
      {/* Add custom CSS for markdown styling */}
      <style jsx global>{`
        .markdown-dark h1, .markdown-dark h2, .markdown-dark h3, 
        .markdown-dark h4, .markdown-dark h5, .markdown-dark h6 {
          color: #e2e8f0;
          margin-top: 1rem;
          margin-bottom: 0.5rem;
          font-weight: bold;
        }
        .markdown-dark h1 { font-size: 1.8rem; }
        .markdown-dark h2 { font-size: 1.5rem; }
        .markdown-dark h3 { font-size: 1.3rem; }
        
        .markdown-light h1, .markdown-light h2, .markdown-light h3,
        .markdown-light h4, .markdown-light h5, .markdown-light h6 {
          color: #1a202c;
          margin-top: 1rem;
          margin-bottom: 0.5rem;
          font-weight: bold;
        }
        .markdown-light h1 { font-size: 1.8rem; }
        .markdown-light h2 { font-size: 1.5rem; }
        .markdown-light h3 { font-size: 1.3rem; }
        
        .markdown-dark p, .markdown-light p {
          margin-bottom: 1rem;
        }
        
        .markdown-dark ul, .markdown-dark ol,
        .markdown-light ul, .markdown-light ol {
          padding-left: 2rem;
          margin-bottom: 1rem;
          list-style-type: disc;
        }
        
        .markdown-dark ol, .markdown-light ol {
          list-style-type: decimal;
        }
        
        .markdown-dark li, .markdown-light li {
          margin-bottom: 0.5rem;
          display: list-item;
        }
        
        .markdown-dark strong {
          color:rgb(0, 0, 0);
          font-weight: bold;
        }
        
        .markdown-light strong {
          color:rgb(0, 0, 0);
          font-weight: bold;
        }
        
        .markdown-dark code, .markdown-light code {
          font-family: monospace;
        }
        
        .markdown-dark code {
          background-color: #2d3748;
          padding: 0.2rem 0.4rem;
          border-radius: 0.25rem;
        }
        
        .markdown-light code {
          background-color: #edf2f7;
          padding: 0.2rem 0.4rem;
          border-radius: 0.25rem;
        }
        
        .whitespace-pre-wrap {
          white-space: pre-wrap;
        }
      `}</style>
    </div>
  );
}