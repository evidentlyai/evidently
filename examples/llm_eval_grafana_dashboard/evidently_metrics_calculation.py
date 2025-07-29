import datetime
import time
import openai
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from evidently import Dataset, DataDefinition, Report
from evidently.presets import TextEvals
from evidently.descriptors import DeclineLLMEval, NegativityLLMEval, SentenceCount, Sentiment 

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

rand = random.Random()
SEND_TIMEOUT = 5
CONNECTION_STRING = "host=localhost port=5432 user=postgres password=example"
CONNECTION_STRING_DB = CONNECTION_STRING + " dbname=test"

create_table_statement = """
drop table if exists llm_metrics;
create table llm_metrics(
	timestamp timestamp,
	negativity text, 
	sentiment float, 
	declines text, 
	sentence_count integer,
	question text, 
	response text, 
	input_tokens integer, 
	output_tokens integer
)
"""

client = openai.OpenAI(
    #api_key="YOUR_KEY_HERE",
)

questions = [
    "What is the chemical symbol for gold?",
    "What is the capital of Japan?",
    "Tell me a joke.",
    "When does water boil?",
    "Who painted the Mona Lisa?",
    "What’s the fastest animal on land?",
    "Can you help me with my math homework?"
    "How many states are there in the USA?",
    "What’s the primary function of the heart?",
    "Can you tell me the latest stock market trends?",
]

def mock_chatbot(client, question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Aswer in 1-3 sentences"},
            {"role": "user", "content": question}
        ],
        temperature=0,
    )

    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    
    result={
        "question": question,
        "response": response.choices[0].message.content.strip(),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }

    return result

descriptors = [
        NegativityLLMEval("response", alias="Negativity"),
        Sentiment("response", alias="Sentiment"),
        DeclineLLMEval("response", alias="Declines"),
        SentenceCount("response", alias="Sentence count")        
    ]

def prep_db():
	with psycopg.connect(CONNECTION_STRING, autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect(CONNECTION_STRING_DB) as conn:
			conn.execute(create_table_statement)

def calculate_metrics_postgresql(i):
	current_result = mock_chatbot(client, questions[i])
	current_dataset = Dataset.from_pandas(
    	pd.DataFrame.from_dict([current_result]),
    	data_definition=DataDefinition(),
    	descriptors=descriptors
	).as_dataframe()
	with psycopg.connect(CONNECTION_STRING_DB, autocommit=True) as conn:
		with conn.cursor() as curr:
			curr.execute(
				"""insert into llm_metrics(timestamp, negativity, sentiment, declines, sentence_count, 
				question, response, input_tokens, output_tokens) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
				(
					datetime.datetime.now(), 
					current_dataset.iloc[0]["Negativity"], 
					current_dataset.iloc[0]["Sentiment"], 
					current_dataset.iloc[0]["Declines"],
					current_dataset.iloc[0]["Sentence count"],
					current_dataset.iloc[0]["question"],
					current_dataset.iloc[0]["response"],
					current_dataset.iloc[0]["input_tokens"],
					current_dataset.iloc[0]["output_tokens"],
				)
			)

def batch_monitoring():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=5)
	for i in range(len(questions)):
		calculate_metrics_postgresql(i)
		new_send = datetime.datetime.now()
		seconds_elapsed = (new_send - last_send).total_seconds()
		if seconds_elapsed < SEND_TIMEOUT:
			time.sleep(SEND_TIMEOUT - seconds_elapsed)
		while last_send < new_send:
			last_send = last_send + datetime.timedelta(seconds=5)
		logging.info("data sent")

if __name__ == '__main__':
	batch_monitoring()
