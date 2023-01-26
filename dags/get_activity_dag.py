from airflow.decorators import dag, task
from pendulum import datetime, duration
import requests
import logging

API = "https://www.boredapi.com/api/activity"

# get Airflow task and processor logger
log = logging.getLogger('airflow.task')


@dag(
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    tags=["Activity"],
    catchup=False,
    dagrun_timeout=duration(hours=1)
)
def get_activity_dag():

    @task
    def get_activity():
        r = requests.get(API)
        return r.json()

    @task 
    def write_activity_to_file(response):
        f = open("include/activity.txt", "a")
        f.write(f"Today you will: {response['activity']}")
        f.close()

    @task 
    def read_activity_from_file():
        f = open("include/activity.txt", "r")
        log.info(f.read(5))
        f.close()

    write_activity_to_file(get_activity()) >> read_activity_from_file()


get_activity_dag()