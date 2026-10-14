from collections import deque

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def is_palindrome(text):
    cleaned = "".join(text.lower().split())

    if not cleaned:
        return False

    stack = list(cleaned)
    queue = deque(cleaned)

    while stack:
        if stack.pop() != queue.popleft():
            return False

    return True


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"text": "", "result": None}
    )


@app.post("/check", response_class=HTMLResponse)
async def check(request: Request, text: str = Form(...)):
    result = is_palindrome(text)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"text": text, "result": result}
    )

