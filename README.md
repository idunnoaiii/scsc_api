# scsc_api
This is application for SCSC system, include:
  - frontend using Vuejs
  - backend using FastAPI framework 
  - database using PostgreSQL
## Requires
  - Nodejs
  - Python3
  - Docker and Docker-compose
  
## Database
Run
```
docker-compose up -d
```
  
## Frontend
Run to start frontend
```
npm run serve
```

## Backend
Run
```
uvicorn app.main:app --host '172.0.0.1' --reload
```
