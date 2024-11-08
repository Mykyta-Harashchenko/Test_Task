Good afternoon, here is my test task
Here are few steps to start my project:

1.Start docker and put this command into terminal to start a PotgreSQL database
docker run --name postgres -e POSTGRES_PASSWORD=12345 -p 5432:5432 -d postgres
2. Install all libraries 
pip install fastapi sqlalchemy asyncpg databases psycopg2 uvicorn alembic
3. Now you can start this project by this command
uvicorn app.main:app --reload
Hope you will like my project, and I will get to next part of interview:)

