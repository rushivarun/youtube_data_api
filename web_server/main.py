import os
import uvicorn
import json
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from rake_nltk import Rake


import mysql.connector


class paginatePayload(BaseModel):
    page_number: int

class searchPayload(BaseModel):
    query: str


db = mysql.connector.connect(host="mysql", user="root", passwd="my_secret_pw", database="yt_api")
mycursor = db.cursor()

r = Rake()

app = FastAPI()

@app.post("/get")
async def paginated(payload: paginatePayload):

    cursor_lead = (payload.page_number*10) - 10
    mycursor.execute('SELECT * FROM Football limit %s, %s', (cursor_lead, 10))
    data = list(mycursor.fetchall())
    print(type(data))
    return json.dumps(data, indent=4)

@app.post("/search")
async def search(payload: searchPayload):

    keywords = r.extract_keywords_from_text(payload.query)
    ranked = r.get_ranked_phrases()

    result = []
    
    for i in ranked:
        search_term = ("%" + i + "%")
        partial_response = mycursor.execute("SELECT * FROM Football WHERE title LIKE \"%s\" OR description LIKE \"%s\"", (search_term, search_term))
        if partial_response == None:
            return "its nothing here"
        else:
            result = result + partial_response

    return json.dumps(result, indent=4)



