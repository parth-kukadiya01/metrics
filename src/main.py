from core.app import app
import uvicorn
from routes import *
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)