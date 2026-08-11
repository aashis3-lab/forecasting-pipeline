from dotenv import load_dotenv
import os
import snowflake.connector as sc
import pandas as pd

load_dotenv()

# -------------connect to snowflake-------------------

conn = sc.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

print("Connected to Snowflake!")

cursor = conn.cursor()
cursor.execute("""
SELECT CURRENT_DATABASE(),
       CURRENT_SCHEMA(),
       CURRENT_ROLE();
""")

row = cursor.fetchone()
print(row)

# we established a stable connection to Snowflake data
# now we wanna pull the table into a DataFrame

query = "SELECT * FROM sales LIMIT 100"
df = pd.read_sql(query, conn) # pulling data into a dataframe

# clean the dataframe
df["MONTH"] = pd.to_datetime(df["MONTH"], errors="coerce")
df = df.dropna(subset=["HISTORY"])
df = df.sort_values(["CUSTOMER","ITEM","MONTH"])

# -------------------connect to claude-------------------

from google import genai
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="say hello"
)

print(response.text)