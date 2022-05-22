# VEND API

### Instalation steps
1. Create new local PostgreSQL database or get data from remote one
2. Create virtualenv on Python 3.10 and activate it
3. Create `.env` file in project root and update variables
4. Install requirements `pip install -r requirements/dev.txt`
5. Create your user `python create_user.py Pero Peric pero.peric@example.com pass1234`
6. Run app and enjoy :)

### Migrations
- Create new migration with `alembic revision --autogenerate -m "Migration name"`
- Apply migrations to db with `alembic upgrade head`
