"""
### Dynamically map over a task group to create files in S3

This DAG dynamically maps over a task group creating files in an S3 bucket.
"""

from airflow.decorators import dag, task_group, task
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator
from pendulum import datetime, duration

import json

MY_S3_BUCKET = "s3://mytxtbucket"
AWS_CONN_ID = "aws_conn"


def return_my_num(num):
    return num


@dag(
    dag_id="upload_files_to_s3",
    start_date=datetime(2022, 12, 1),
    schedule=None,
    catchup=False,
    dagrun_timeout=duration(days=1),
)
def upload_files_to_s3():
    @task_group(group_id="create_s3_files")
    def create_s3_files(num):
        @task
        def return_num_as_int(my_num):
            return my_num

        my_num_as_int = return_num_as_int(num)

        write_to_s3 = S3CreateObjectOperator(
            task_id="write_to_s3",
            aws_conn_id=AWS_CONN_ID,
            data=json.dumps(f"{my_num_as_int}"),
            replace=True,
            s3_key=f"{MY_S3_BUCKET}/{my_num_as_int}.txt",
        )

        my_num_as_int >> write_to_s3

    create_s3_files.expand(num=[0, 1, 2, 3, 4, 5])


upload_files_to_s3()
