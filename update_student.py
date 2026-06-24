from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(
        text(""" UPDATE students
     SET age = :age
     WHERE id = :id"""),
        {
            "age": 21,
            "id": 1
        }
    )
    conn.commit()
print("Student Updated Successfully")