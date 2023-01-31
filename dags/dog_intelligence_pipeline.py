"""
dog_intelligence_pipeline
DAG auto-generated by Astro Cloud IDE.
"""

from airflow.decorators import dag
from astro import sql as aql
from astro.sql.table import Table
import pandas as pd
import pendulum


@aql.dataframe(task_id="model_task")
def model_task_func(transform_table: pd.DataFrame):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    
    # use the table returned from the transform_table cell
    df = transform_table
    
    # calculate baseline accuracy
    baseline_accuracy = df.iloc[:,-1].value_counts(normalize=True)[0]
    
    # selecting predictors (X) and the target (y)
    X = df.iloc[:,:-1]
    y = df.iloc[:,-1]
    
    # split the data into training data (80%) and testing data (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=23
    )
    
    # standardize features
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    
    # train a RandomForestClassifier on the training data
    model = RandomForestClassifier(max_depth=3, random_state=19)
    model.fit(X_train_s, y_train)
    
    # score the trained model on the testing data
    score = model.score(X_test_s, y_test)
    
    # get feature importances
    feature_importances = list(zip(X_train.columns, model.feature_importances_))
    
    return f"baseline accuracy: {baseline_accuracy}", f"model accuracy: {score}", feature_importances 

@aql.transform(conn_id="snowflake_conn", task_id="query_table")
def query_table_func():
    return """-- Write your SQL query here
SELECT * FROM SANDBOX.TAMARAFINGERLIN.DOG_INTELLIGENCE 
WHERE CONCAT(BREED, HEIGHT_LOW_INCHES, HEIGHT_HIGH_INCHES, 
WEIGHT_LOW_LBS, WEIGHT_HIGH_LBS, REPS_UPPER, REPS_LOWER) IS NOT NULL"""

@aql.transform(conn_id="snowflake_conn", task_id="transform_table")
def transform_table_func(query_table: Table):
    return """-- Write your SQL query here
SELECT HEIGHT_LOW_INCHES, HEIGHT_HIGH_INCHES, WEIGHT_LOW_LBS, WEIGHT_HIGH_LBS,
    CASE WHEN reps_upper <= 25 THEN 'very_smart_dog'
    ELSE 'smart_dog'
    END AS INTELLIGENCE_CATEGORY
FROM {{query_table}}"""

@dag(
    schedule_interval=None,
    start_date=pendulum.from_format("2022-11-03", "YYYY-MM-DD"),
    dagrun_timeout=pendulum.duration(hours=3)
)
def dog_intelligence():
    query_table = query_table_func()

    transform_table = transform_table_func(
        query_table,
    )

    model_task = model_task_func(
        transform_table,
    )

    model_task << transform_table

    transform_table << query_table

dag_obj = dog_intelligence()