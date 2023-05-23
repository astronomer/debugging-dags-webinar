Overview
========

Welcome! This repository contains 3 example DAGs that were used in the Astronomer [Debugging your Airflow DAGs](https://www.astronomer.io/events/webinars/debugging-your-airflow-dags/) webinar.

## How to run this repository

Download the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally in Docker. `astro` is the only package you will need to install.

1. Run `git clone https://github.com/astronomer/debugging-dags-webinar.git` on your computer to create a local clone of this repository.
2. Install the Astro CLI by following the steps in the [Astro CLI documentation](https://docs.astronomer.io/astro/cli/install-cli). The main prerequisite is Docker Desktop/Docker Engine but no Docker knowledge is needed to run Airflow with the Astro CLI.
3. Run `astro dev start` in your cloned repository.
4. After your Astro project has started. View the Airflow UI at `localhost:8080`.

## DAGs

- `dog_intelligence_pipeline`: This DAG was generated using the [Astronomer Cloud IDE](https://docs.astronomer.io/astro/cloud-ide). It runs a small ML pipeline that tries to predict dog intelligence based on dog weight and height. You will need to set up a connection to a relational database to run this DAG, see the first steps in the [companion tutorial](https://docs.astronomer.io/learn/cloud-ide-tutorial).
- `get_activity_dag`: fetches an activity from the https://www.boredapi.com/api/activity. This DAG does not need any connections to run.
- `upload_files_to_s3`: creates files in an S3 bucket. This DAG needs an AWS connection and an S3 bucket to run.