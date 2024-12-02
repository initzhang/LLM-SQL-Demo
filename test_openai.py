import llmsql
from llmsql.llm.openai import OpenAI
llmsql.init(OpenAI(base_url="http://0.0.0.0:8000/v1", api_key="abc123", model="meta-llama/Meta-Llama-3-8B-Instruct"))


# Make sure you import duckdb from llmsql
from llmsql.duckdb import duckdb

# Create a table from the movies dataset
conn = duckdb.connect(database=':memory:', read_only=False)
conn.execute("CREATE TABLE movies AS SELECT * FROM read_csv('./examples/duckdb/movies_small.csv')")
conn.execute("CREATE TABLE movies_limit as SELECT * FROM movies WHERE review_content IS NOT NULL LIMIT 20")

conn.sql("SHOW TABLES")

conn.sql("DESCRIBE movies_limit")

query = ("SELECT review_content, LLM('Given a movie review as {review_content}, classify the review as either POSITIVE, NEGATIVE, or NEUTRAL." 
         "Respond with just the category and no other text.', review_content) AS sentiment FROM movies_limit")
conn.sql(query).show()
