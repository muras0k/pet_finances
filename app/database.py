from psycopg_pool import ConnectionPool

DATABASE_URL = 'postgresql://postgres@localhost:5432/fastapi'

pool = ConnectionPool(conninfo=DATABASE_URL)