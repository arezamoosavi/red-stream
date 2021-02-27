import os

from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import (
    Table,
    Column,
    Integer,
    BigInteger,
    DateTime,
    MetaData,
    Text,
    Float,
)
from sqlalchemy.sql import text, func

SQL_HOST = os.getenv("SQL_HOST")
SQL_PORT = int(os.getenv("SQL_PORT"))
SQL_USER = os.getenv("SQL_USER")
SQL_PASS = os.getenv("SQL_PASS")
SQL_DB = os.getenv("SQL_DB")

engine = create_engine(
    "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset=utf8mb4".format(
        SQL_USER, SQL_PASS, SQL_HOST, SQL_PORT, SQL_DB
    )
)


metadata = MetaData()

bitcoin_model = Table(
    "bitcoin_model",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("open", Float, nullable=True, default=""),
    Column("high", Float, nullable=True, default=""),
    Column("low", Float, nullable=True, default=""),
    Column("close", Float, nullable=True, default=""),
    Column("1step_close", Float, nullable=True, default=""),
    Column("10step_close", Float, nullable=True, default=""),
)

metadata.create_all(engine)
inspector = inspect(engine)


def insert_json_data(data, table_name):
    with engine.connect() as con:
        statement = lambda x: text(
            """INSERT INTO {}({}) VALUES(:{})""".format(
                table_name, ",  ".join(x), ", :".join(x)
            )
        )

        con.execute(statement(data), **data)


def update_json_data(data, table_name):
    with engine.connect() as con:
        # create SET:
        set_data = ""
        for k, v in data["update_data"].items():
            set_data += "{} = '{}',".format(k, v)

        query = """Update {} set {} where {} = '{}'""".format(
            table_name, set_data[:-1], data["pk_field"], data[data["pk_field"]]
        )

        con.execute(text(query))


def get_data_if_exists(field_val: dict, table_name: str):
    with engine.connect() as con:
        query = """SELECT * FROM {} WHERE {} = '{}'""".format(
            table_name, field_val["pk_field"], field_val["pk_val"]
        )
        result = con.execute(query).first()
        json_res = dict(result.items()) if result else None
        return json_res
