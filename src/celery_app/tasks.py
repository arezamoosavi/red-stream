import logging
import traceback

logging.info("logs started . . .")
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | {%(pathname)s:%(lineno)d} | %(module)s | %(levelname)s | %(funcName)s | %(message)s",
)

from .app import app as celery_app
from utils.mysql_db import insert_json_data
from joblib import load
import csv

data_cols = ["Open", "High", "Low", "Close"]
data_path = "utils/ml/bitcoin_test.csv"


def read_csv_data(path, columns):
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = dict(row)
            yield {k.lower(): float(data[k]) for k in columns}


gen_data = read_csv_data(data_path, data_cols)
loaded_mdl = load('utils/ml/mimo_gbr.joblib')


@celery_app.task
def run_model_evaluation():
    dict_data = next(gen_data, None)
    if dict_data is None:
        return None

    try:
        result = loaded_mdl.predict([[dict_data["open"], dict_data["high"], dict_data["low"]]])
        dict_data["1step_close"] = result[0][0]
        dict_data["10step_close"] = result[0][1]

        insert_json_data(dict_data, "bitcoin_model")

    except Exception as e:
        trace = traceback.format_exc().replace('\n', '  ')
        logging.error(f"{trace}")
        return trace

    return dict_data


celery_app.conf.beat_schedule = {
    "add-every-5-seconds": {
        "task": "celery_app.tasks.run_model_evaluation",
        "schedule": 5.0,
    },
}
