from fastapi import FastAPI, HTTPException, Depends
from fastapi_model import IssueAddRequest, AssgineeSearchRequest
from fastapi_service import load_faiss_cpu_db, search_faiss_cpu_db, add_faiss_cpu_db

app = FastAPI()

@app.on_event("startup")
async def load_db():
    global db
    db = await load_faiss_cpu_db('SWE_ASYNC_DB_INDEX')

@app.post("/issue/")
async def add_issue(issue: IssueAddRequest):
    query = issue.title + " " + issue.description
    await add_faiss_cpu_db(query, issue.assignee_id, issue.fixer_id, db)
    return {"message": "Issue added successfully"}

@app.get("/assignee/")
async def get_assignee(issue: AssgineeSearchRequest = Depends()):
    query = issue.title + " " + issue.description
    results = await search_faiss_cpu_db(query, db)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"assignees": results}

