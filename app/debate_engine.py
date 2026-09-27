import re

from app.provider import ask_model
from app.prompt_loader import load_prompt


def run_debate(statement: str):

    pro_template = load_prompt("pro.txt")
    con_template = load_prompt("cons.txt")
    arbiter_template = load_prompt("arbiter.txt")

    pro_prompt = pro_template.format(
        statement=statement
    )

    con_prompt = con_template.format(
        statement=statement
    )

    pro = ask_model(pro_prompt)

    con = ask_model(con_prompt)

    arbiter_prompt = arbiter_template.format(
        statement=statement,
        pro=pro[:1000],
        con=con[:1000]
    )

    arbiter = ask_model(arbiter_prompt)

    pro_match = re.search(
        r"PRO SCORE:\s*(\d+)",
        arbiter,
        re.IGNORECASE
    )

    con_match = re.search(
        r"CON SCORE:\s*(\d+)",
        arbiter,
        re.IGNORECASE
    )

    pro_score = int(pro_match.group(1)) if pro_match else 0
    con_score = int(con_match.group(1)) if con_match else 0

    winner = "PRO" if pro_score >= con_score else "CON"

    return {
        "pro": pro,
        "con": con,
        "arbiter": arbiter,
        "winner": winner,
        "pro_score": pro_score,
        "con_score": con_score
    }