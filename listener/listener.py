from fastapi import FastAPI, Request
import uvicorn
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


app=FastAPI()

@app.get("/")
def root(cookie:str, request:Request):
    print(f"{Fore.RED} New cookie received > ", cookie)
    return "Thanks"

if __name__ == "__main__":
    print("listening for cookies...")
    uvicorn.run("listener:app", host="0.0.0.0", port=8081, log_level="warning", reload=True)
