from worker.celery_app import celery_app
from googleapiclient.discovery import build
import json
import mysql.connector
from datetime import timedelta, datetime, timezone

import logging

api_key = "AIzaSyAI-ST49GD3voArhrTmIfsRYid5IvG6tgM"

youtube = build("youtube", "v3", developerKey=api_key)

db = mysql.connector.connect(host="0.0.0.0", user="root", passwd="my-secret-pw", database="yt_api")
mycursor = db.cursor()

celery_app.conf.beat_schedule = {
        'youtube-beat': {
            'task': 'youtube_dialer',
            'schedule': timedelta(seconds=10)
        },
    }

def sql_instert_gen(snippet):
    title = snippet["title"]
    description = snippet["description"]
    publishedAt = snippet["publishedAt"]

    # Preparing SQL query to INSERT a record into the database.
    insert_stmt = "INSERT INTO Football (title, description, publishedAT) VALUES (%s, %s, %s)"
    data = (title, description, publishedAt)

    try:
        # Executing the SQL command
        mycursor.execute(insert_stmt, data)
    
        # Commit your changes in the database
        db.commit()

    except:
        # Rolling back in case of error
        db.rollback()

    # print("Data inserted")


    # mycursor.execute("INSERT INTO Football1 (title, description, publishedAT) VALUES (%s, %s, %s)", (title, description, publishedAt))
    # db.commit()
    return True


@celery_app.task(name="youtube_dialer")
def youtube_dialer():
    latest_timestamp_arg = datetime.now(timezone.utc) - timedelta(hours=0, minutes=0, seconds=30)
    print(latest_timestamp_arg)
    temp = latest_timestamp_arg.astimezone()
    time_to_check = temp.isoformat()

    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q="football",
        publishedAfter=time_to_check
    )

    response = request.execute()

    if len(response["items"]) > 0:
        for i in response["items"]:
            snippet = i["snippet"]
            insert_command = sql_instert_gen(snippet)
        return "added"

    else:
        return "wait pls"