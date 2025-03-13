from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retrieve import get_query_result

app = FastAPI()

# Add CORS middleware with expanded configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://172.22.48.1:3000", "http://10.110.107.217:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def my_query_endpoint(query: QueryRequest):
    return await get_query_result(query)

# Add this code to run the server when the file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # 8000 is already in use from Milvus
