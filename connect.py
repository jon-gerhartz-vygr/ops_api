from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv
import os
import pandas as pd
import snowflake.connector


load_dotenv()
DB = os.getenv("DB")
SCHEMA = os.getenv("SCHEMA")
SNOWFLAKE_ACCOUNT_ID = os.getenv("SNOWFLAKE_ACCOUNT_ID")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PRIVATE_KEY_PASSPHRASE = os.getenv('PRIVATE_KEY_PASSPHRASE')

private_key_pem = PRIVATE_KEY.replace("\\n", "\n")

p_key = serialization.load_pem_private_key(
    private_key_pem.encode(),
    password=PRIVATE_KEY_PASSPHRASE.encode(),
    backend=default_backend()
)

pkb = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())


def connect_to_sf():
    ctx = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        account=SNOWFLAKE_ACCOUNT_ID,
        private_key=pkb,
        database=DB,
        schema=SCHEMA
    )
    return ctx


def execute_query(query):
    ctx = connect_to_sf()
    cur = ctx.cursor()
    cur.execute(query)
    result = cur.fetchall()
    ctx.close()
    return result


def fetch_pandas(query):
    ctx = connect_to_sf()
    cur = ctx.cursor()
    cur.execute(query)
    df = cur.fetch_pandas_all()
    ctx.close()
    return df
