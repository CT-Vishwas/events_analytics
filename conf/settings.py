from dotenv import load_dotenv
import os

load_dotenv()
dburl = os.getenv('DBURL','DBURL Not Available')
print(dburl)