"use client"

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

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
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Ask a Question</h1>
      <form onSubmit={handleSubmit} className="mb-6">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your question"
          className="border p-2 mr-2 w-64"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="bg-blue-500 text-white p-2 rounded"
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Submit"}
        </button>
      </form>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      {isLoading && <div>Processing your question...</div>}

      {response && !isLoading && (
        <div className="bg-white-100 p-4 rounded">
          <h2 className="text-xl font-semibold mb-2">Answer:</h2>
          <p className="mb-4">{response.answer}</p>
          
          {response.sources && (
            <>
              <h3 className="text-lg font-semibold mb-2">Sources:</h3>
              <div className="bg-black p-2 rounded overflow-auto max-h-64">
                <pre className="whitespace-pre-wrap">{JSON.stringify(response.sources, null, 2)}</pre>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}