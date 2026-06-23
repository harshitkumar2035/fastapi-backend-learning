from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(
        text("""
            INSERT INTO students (name, age)
            VALUES (:name, :age)
        """),
        {
            "name": "Harshit",
            "age": 20
        }
    )
    conn.commit()
print("Student Added Successfully")