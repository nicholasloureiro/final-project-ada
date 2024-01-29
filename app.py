# app.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import psycopg2

app = FastAPI()

# PostgreSQL configurations
db_config = {
    'host': 'db',
    'user': 'postgres',
    'password': 'changeme',
    'database': 'postgres',
}
def create_table():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task VARCHAR(255) NOT NULL
        )
        
    """)

    connection.commit()
    cursor.close()
    connection.close()

def insert_sample_data():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    
    cursor.execute("INSERT INTO tasks (task) VALUES ('Lavar a roupa')")
    

    connection.commit()
    cursor.close()
    connection.close()

def delete_sample_data():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    
    cursor.execute("DELETE FROM tasks")

    connection.commit()
    cursor.close()
    connection.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <h1>Hello, Wilton! Hope you like it!</h1>
    <br>
    <ul>
        <li><a href="/">Home</a></li>
        <br>
        <li><a href="/init">Init DB</a></li>
        <br>
        <li><a href="/insert">Insert tasks</a></li>
        <br>
        <li><a href="/delete">Clear DB</a></li>
        <br>
        <li><a href="/search">Mostra os dados do BD</a></li>
    </ul>
    """

@app.get("/init")
def init_db():
    create_table()
    return "Success"

@app.get("/insert")
def insert_sample_data_route():
    insert_sample_data()
    return "New data inserted!"

@app.get("/delete")
def delete_sample_data_route():
    delete_sample_data()
    return "DB cleared!"

@app.get("/search", response_class=HTMLResponse)
def fetch_data():
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

  
    cursor.execute("SELECT task FROM tasks")
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    result = "<h1>Search:</h1><ul>"
    for row in data:
        result += f"<li>{row}</li>"
    result += "</ul>"

    return HTMLResponse(content=result)

if __name__ == "__main__":
    create_table()         
    insert_sample_data()
