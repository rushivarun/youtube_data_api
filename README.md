# youtube_data_api

## Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.
- 
## Build Instructions
### Simple installation
```
docker-compose up
```
## Build applictions individually
### To trigger the periodic Youtube API ping
```
cd app
```
```
docker-compose up
```
### To start the web-server running on FAST API to connect to the mysql db
```
cd web-server
```
```
docker-compose up
```
### No DockerCompose Installation
MySQL DB for holding data
```
docker run -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 mysql
```
Redis for broker and backend to Celery
```
docker run -it --rm --name redis --net redis -p 6379:6379 redis:6.0-alpine
```
```
cd app
```
Initiate the Celery workers and Beat.
```
celery -A worker.celery_worker worker -l info
```
```
celery -A worker.celery_worker beat -l info
```
```
cd ../web-server
```
Run the web server.
```
uvicorn main:app --reload
```
