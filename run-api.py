# Author: Richard Sun
# run.py
import uvicorn
from api.config import HOST, PORT

if __name__ == "__main__":
    uvicorn.run("api.main:app", host=HOST, port=PORT)