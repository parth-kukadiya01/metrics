from core.app import app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
