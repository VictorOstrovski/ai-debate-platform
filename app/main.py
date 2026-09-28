from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.debate_engine import run_debate

from app.database import (
    init_db,
    save_debate,
    get_all_debates,
    get_debate_by_id
)

app = FastAPI()

init_db()

templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/debate", response_class=HTMLResponse)
async def debate(request: Request, question: str = Form(...)):

    result = run_debate(question)

    debate_id = save_debate(
        statement=question,
        pro=result["pro"],
        con=result["con"],
        arbiter=result["arbiter"]
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "question": question,
            "pro": result["pro"],
            "con": result["con"],
            "arbiter": result["arbiter"],
            "winner": result["winner"],
            "pro_score": result["pro_score"],
            "con_score": result["con_score"],
            "russian_translation": result["russian_translation"],
            "debate_id": debate_id
        }
    )


@app.get("/prompts", response_class=HTMLResponse)
async def prompts_page(request: Request):

    prompts_dir = Path("app/prompts")

    pro = (prompts_dir / "pro.txt").read_text(
        encoding="utf-8"
    )

    con = (prompts_dir / "cons.txt").read_text(
        encoding="utf-8"
    )

    arbiter = (prompts_dir / "arbiter.txt").read_text(
        encoding="utf-8"
    )

    return templates.TemplateResponse(
        request=request,
        name="prompts.html",
        context={
            "pro": pro,
            "con": con,
            "arbiter": arbiter,
            "saved": False
        }
    )


@app.post("/prompts", response_class=HTMLResponse)
async def save_prompts(
    request: Request,
    pro: str = Form(...),
    con: str = Form(...),
    arbiter: str = Form(...)
):

    prompts_dir = Path("app/prompts")

    (prompts_dir / "pro.txt").write_text(
        pro,
        encoding="utf-8"
    )

    (prompts_dir / "cons.txt").write_text(
        con,
        encoding="utf-8"
    )

    (prompts_dir / "arbiter.txt").write_text(
        arbiter,
        encoding="utf-8"
    )

    return templates.TemplateResponse(
        request=request,
        name="prompts.html",
        context={
            "pro": pro,
            "con": con,
            "arbiter": arbiter,
            "saved": True
        }
    )


@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    debates = get_all_debates()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "debates": debates
        }
    )


@app.get("/history/{debate_id}", response_class=HTMLResponse)
async def debate_details(
    request: Request,
    debate_id: int
):

    debate = get_debate_by_id(debate_id)

    return templates.TemplateResponse(
        request=request,
        name="saved_debate.html",
        context={
            "debate": debate
        }
    )