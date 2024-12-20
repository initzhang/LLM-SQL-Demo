# LLM-SQL

install dependencies in requirements.txt

call LLM through API:
```
# in a separate console
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-8B-Instruct --dtype auto --api-key abc123
# in current console
python test_openai.py
```

call LLM as internal function:
```
python test_vllm.py
```

===========

`llmsql` provides APIs to run LLM queries as UDF operators in relational dataframes or SQL tables.

Supported data formats:
- Pandas
- DuckDB

Support LLM backends:
- OpenAI
- vLLM

## Installation
```bash
# Install llmsql package with OpenAI dependencies
pip install git+https://github.com/lynnliu030/LLM-SQL-Demo.git

# Install llmsql package with vLLM dependencies
pip install git+https://github.com/lynnliu030/LLM-SQL-Demo.git#egg=llmsql[vllm]
``` 

## DuckDB
Run LLM UDFs directly in DuckDB SQL queries through `llmsql.duckdb` API.

```python
import llmsql
from llmsql.llm.openai import OpenAI

llmsql.init(OpenAI(base_url="https://api.openai.com/v1", api_key="OPENAI_API_KEY"))

from llmsql.duckdb import duckdb

conn = duckdb.connect(database=':memory:')
conn.execute("CREATE TABLE example_table (example_column INT, example_column_2 INT)")
conn.execute("INSERT INTO example_table VALUES (1, 1)")

conn.sql(
    "SELECT LLM('Add {example_column} and {example_column_2}. Return just a number with no additional text.', example_column, example_column_2) from example_table")
```

See `examples/duckdb` for more examples.

## Pandas
Run LLM queries as UDFs on Pandas Dataframes via the `llmsql.pandas` API.

```python
import llmsql
from llmsql.llm.openai import OpenAI

llmsql.init(OpenAI(base_url="https://api.openai.com/v1", api_key="OPENAI_API_KEY"))

import llmsql.pandas
import pandas as pd

df = pd.DataFrame({"example_column": [1, 2], "example_column_2": [1, 2]})
df.llm_query(
    "Add {example_column} and {example_column_2}. Return just a number with no additional text.")
```

See `examples/pandas` for more examples.

## Optimizations
Various optimizations as described in ["Optimizing LLM Queries in Relational Workloads"](https://arxiv.org/pdf/2403.05821) have been implemented in the Pandas API.

**Column reordering**: The order of the fields that are provided to the LLMs are reordered to maximize KV cache hits for prefixes. Fields with shorter average string length and less unique number of values are placed first in the prompt.

**Row reordering** Rows in the table are lexicographically sorted to maximize KV cache hits for prefixes.

