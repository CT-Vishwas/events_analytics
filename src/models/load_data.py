from sqlalchemy import create_engine

engine = create_engine(f"sqlite://C:\\Users\\VishwasKSingh\\Workspace\\temp\\my_app\\dbs\\myfile.db")

with engine.connect() as conn:
    query = "CREATE TABLE IF NOT EXISTS events(id INT, name TEXT)"
    conn.execute(query)
    conn.commit()