#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example DAG which uses SparkKubernetesOperator and SparkKubernetesSensor.
In this example, we create two tasks which execute sequentially.
The first task is to submit sparkApplication on Kubernetes cluster(the example uses
spark-pi application).
and the second task is to check the final state of the sparkApplication that submitted
in the first state.
Spark-on-k8s operator is required to be already installed on Kubernetes
https://github.com/GoogleCloudPlatform/spark-on-k8s-operator
"""

from datetime import timedelta

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor, S3KeysUnchangedSensor

# Operators; we need this to operate!
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import (
    SparkKubernetesSensor,
)
from airflow.utils.dates import days_ago

# [END import_module]

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "Gersonrs",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["gersonrodriguessantos8@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 1,
    "retry_delay": timedelta(1),
}
# [END default_args]

# [START instantiate_dag]

dag = DAG(
    "pipeline-delta-lake-deep-dive-complete",
    default_args=default_args,
    schedule_interval="@once",
    tags=["spark", "kubernetes", "s3", "sensor", "minio", "bronze", "silver"],
)
# [END instantiate_dag]

# [START set_tasks]

start = DummyOperator(task_id='start', dag=dag)

# verify if new data has arrived on processing bucket
# connecting to minio to check (sensor)
list_keys = S3ListOperator(
    task_id="list_keys",
    bucket="landing",
    prefix="/",
    aws_conn_id="minio",
    do_xcom_push=True,
    dag=dag,
)

ingestion = SparkKubernetesOperator(
    task_id="task_spark_ingestion_file_local_to_bronze_table",
    namespace="processing",
    application_file="spark_jobs/ingestion_from_local_data_file_to_bronze_tables.yaml",
    kubernetes_conn_id="kubernetes_default",
    do_xcom_push=True,
    dag=dag,
)

ingestion_sensor = SparkKubernetesSensor(
    task_id="task_spark_ingestion_file_local_to_bronze_table_monitor",
    namespace="processing",
    application_name="{{task_instance.xcom_pull(task_ids='task_spark_ingestion_file_local_to_bronze_table')['metadata']['name']}}",
    kubernetes_conn_id="kubernetes_default",
    dag=dag,
    attach_log=True,
)

maybe_great_expectation = DummyOperator(task_id='maybe_great_expectation', dag=dag)

tranform = SparkKubernetesOperator(
    task_id="task_spark_transform_and_enrichment_from_bronze_to_silver",
    namespace="processing",
    application_file="spark_jobs/transform_and_enrichment_from_bronze_to_silver.yaml",
    kubernetes_conn_id="kubernetes_default",
    do_xcom_push=True,
    dag=dag,
)

transform_sensor = SparkKubernetesSensor(
    task_id="task_spark_transform_and_enrichment_from_bronze_to_silver_monitor",
    namespace="processing",
    application_name="{{task_instance.xcom_pull(task_ids='task_spark_transform_and_enrichment_from_bronze_to_silver')['metadata']['name']}}",
    kubernetes_conn_id="kubernetes_default",
    dag=dag,
    attach_log=True,
)

delivery = SparkKubernetesOperator(
    task_id="task_spark_delivery_data_from_silver_to_gold",
    namespace="processing",
    application_file="spark_jobs/delivery_data_from_silver_to_gold.yaml",
    kubernetes_conn_id="kubernetes_default",
    do_xcom_push=True,
    dag=dag,
)

delivery_sensor = SparkKubernetesSensor(
    task_id="task_spark_delivery_data_from_silver_to_gold_monitor",
    namespace="processing",
    application_name="{{task_instance.xcom_pull(task_ids='task_spark_delivery_data_from_silver_to_gold')['metadata']['name']}}",
    kubernetes_conn_id="kubernetes_default",
    dag=dag,
    attach_log=True,
)

end = DummyOperator(task_id='end', dag=dag)
# [END set_tasks]
# [START task_sequence]
(
    start
    >> list_keys
    >> ingestion
    >> ingestion_sensor
    >> maybe_great_expectation
    >> tranform
    >> transform_sensor
    >> delivery
    >> delivery_sensor
    >> end
)
# [END task_sequence]
