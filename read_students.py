from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT * FROM students")
    )
    for row in result:
        print(row)