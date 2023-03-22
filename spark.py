from os.path import abspath

from delta import *
from pyspark import SparkConf
from pyspark.sql import SparkSession

# set default location for warehouse
warehouse_location = abspath("spark-warehouse")
spark = (
    SparkSession.builder.appName("transform_and_enrichment_from_bronze_to_silver")
    .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .enableHiveSupport()
    .getOrCreate()
)

# show configured parameters
print(SparkConf().getAll())

# set log level
spark.sparkContext.setLogLevel("INFO")
