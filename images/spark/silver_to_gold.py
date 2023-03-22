# import libraries
from os.path import abspath

from delta import DeltaTable
from pyspark import SparkConf
from pyspark.sql import SparkSession

# set default location for warehouse
warehouse_location = abspath("spark-warehouse")

# main spark program
if __name__ == "__main__":
    # init session
    spark = (
        SparkSession.builder.appName("etl-yelp-py")
        .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
        .enableHiveSupport()
        .getOrCreate()
    )

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    get_voters = "s3a://lakehouse/silver/voters"
    get_subscribers = "s3a://lakehouse/silver/subscribers"

    # read user data
    # df_silver_voters = spark.read.format("delta").format("delta").load(get_voters)
    # df_silver_subscribers =
    # spark.read.format("delta").format("delta").load(get_subscribers)
    df_silver_voters = DeltaTable.forPath(spark, get_voters)
    df_silver_subscribers = DeltaTable.forPath(spark, get_subscribers)

    # save dataframe into postgres
    # yugabytedb database [ysql]
    # k8s cluster ip for yugabytedb [intra-communication]
    """
    df_join \
        .write \
        .format("jdbc") \
        .mode("overwrite") \
        .option("url", "jdbc:postgresql://10.0.206.213:5433/owshq") \
        .option("dbtable", "public.fact_reviews") \
        .option("user", "yugabyte") \
        .option("password", "yugabyte") \
        .save()
    """

    # write into parquet file on curated zone
    # file to be available for virtualization engine
    # using minio as storage inside of [k8s]
    df_join.write.format("parquet").mode("overwrite").save(
        "s3a://curated-zone/fact_reviews/"
    )

    # stop session
    spark.stop()
