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

    return {
        "pro": pro,
        "con": con,
        "arbiter": arbiter
    }