from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text(""" 
         CREATE TABLE students (
                 id INT PRIMARY KEY AUTO_INCREMENT,
                 name VARCHAR(100),
                    age INT
         )            
                      
                      """))
    conn.commit()

print    ("Table created successfully")