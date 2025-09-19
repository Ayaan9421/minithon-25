from fastapi import FastAPI
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ Load .env file
load_dotenv()

app = FastAPI()

# ✅ Get Hugging Face token from environment
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in .env")

# ✅ Configure HuggingFace LLM with token
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b", 
    task="text-generation",
    huggingfacehub_api_token=hf_token,  # required!
)

model = ChatHuggingFace(llm=llm)

# ✅ Fix CORS (works for file://, localhost, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # allow both real origins and file://
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    prompt: str

@app.post("/ai_insights")
async def ai_insights(query: Query):
    try:
        # ✅ Ensure model returns something usable
        result = model.invoke(query.prompt)
        return {"response": result.content if hasattr(result, "content") else str(result)}
    except Exception as e:
        # ✅ Debug friendly error response
        return {"error": str(e)}

if __name__ == "__main__":
    # ✅ Use 0.0.0.0 so frontend can reach it
    uvicorn.run(app, host="0.0.0.0", port=8000)