"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch("http://127.0.0.1:8001/query/", {
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
      setResponse(data);
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to get response. Please check if the backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`flex justify-center items-center h-screen transition-all duration-300 ${darkMode ? "bg-black text-white" : "bg-white text-black"}`}>
      {/* Dark Mode Toggle Button */}
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="absolute top-4 left-4 p-2 bg-gray-800 text-white rounded-lg shadow-md hover:bg-gray-700 transition"
      >
        {darkMode ? "Light Mode 🌞" : "Dark Mode 🌙"}
      </button>

      {/* Form Container */}
      <div className={`p-6 rounded-lg shadow-lg text-center w-96 ${darkMode ? "bg-gray-900" : "bg-gray-100"}`}>
        <h1 className="text-2xl font-bold mb-4">Ask a Question</h1>
        <form onSubmit={handleSubmit} className="mb-6">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question"
            className={`border p-2 mr-2 w-full rounded ${darkMode ? "bg-gray-800 text-white border-gray-600" : "bg-gray-200 text-black border-gray-300"}`}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="bg-blue-500 text-white p-2 rounded w-full mt-2"
            disabled={isLoading}
          >
            {isLoading ? "Loading..." : "Submit"}
          </button>
        </form>

        {error && <div className="text-red-500 mb-4">{error}</div>}

        {isLoading && <div>Processing your question...</div>}

        {response && !isLoading && (
          <div className={`p-4 rounded ${darkMode ? "bg-gray-800 text-white" : "bg-gray-100 text-black"}`}>
            <h2 className="text-xl font-semibold mb-2">Answer:</h2>
            <p className="mb-4">{response.answer}</p>

            {response.sources && (
              <>
                <h3 className="text-lg font-semibold mb-2">Sources:</h3>
                <div className={`p-2 rounded overflow-auto max-h-64 ${darkMode ? "bg-gray-700 text-white" : "bg-gray-300 text-black"}`}>
                  <pre className="whitespace-pre-wrap">{JSON.stringify(response.sources, null, 2)}</pre>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
