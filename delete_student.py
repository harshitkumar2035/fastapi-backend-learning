from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(
        text("""DELETE FROM students WHERE id = :id """),
        { "id": 1}
    )
    conn.commit()
print("Student Deleted Successfully")