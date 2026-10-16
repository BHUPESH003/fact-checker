import csv, glob, json, os
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai

load_dotenv()
# LangSmith tracing is on via LANGSMITH_TRACING=true + LANGSMITH_API_KEY in .env
client = wrap_openai(OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPEN_ROUTER_KEY"]))
MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")

PROMPT = """Fact-check this claim using web search, relying only on authoritative sources
(official AWS pages/blogs/docs first). Claim: "{claim}" (service: {service}; claimed origin: {url}).
Reply with JSON only: {{"verdict": "TRUE|FALSE|UNVERIFIABLE", "evidence_url": "...", "reasoning": "one or two sentences"}}"""

@traceable(name="check_claim")
def check(row):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT.format(claim=row["claim_text"], service=row["claimed_service"], url=row["origin_source_url"])}],
        extra_body={"plugins": [{"id": "web", "max_results": 5}]},  # OpenRouter web search
    )
    txt = r.choices[0].message.content.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return {"verdict": "UNVERIFIABLE", "evidence_url": "", "reasoning": f"unparseable: {txt[:200]}"}

if __name__ == "__main__":
    src = glob.glob("data/*.csv")[0]
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    out = [{**r, **check(r)} for r in rows]
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=out[0].keys()); w.writeheader(); w.writerows(out)
    for r in out:
        print(r["candidate_id"], r["verdict"], "-", r["reasoning"])
