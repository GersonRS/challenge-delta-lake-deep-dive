# import libraries
from os.path import abspath

from pyspark import SparkConf
from pyspark.sql import SparkSession

# set default location for warehouse
warehouse_location = abspath("spark-warehouse")

# main spark program
if __name__ == "__main__":
    # init session
    spark = (
        SparkSession.builder.appName("ingestion-to-bronze")
        .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
        .config("spark.hadoop.fs.s3a.endpoint", "http://10.108.233.87:9000")
        .config("spark.hadoop.fs.s3a.access.key", "gerson")
        .config("spark.hadoop.fs.s3a.secret.key", "rHasMuUFzGY0REI2H6RcdaJFNZp9b9ht")
        .config("spark.hadoop.fs.s3a.path.style.access", True)
        .config("spark.hadoop.fs.s3a.fast.upload", True)
        .config("spark.hadoop.fs.s3a.connection.maximum", 100)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.delta.logStore.class",
            "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore",
        )
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

    # set dynamic input file [hard-coded]
    # can be changed for input parameters [spark-submit]
    get_users_file = "/app/landing/user/*.json"
    get_subscription_file = "/app/landing/subscription/*.json"
    get_credit_card_file = "/app/landing/credit_card/*.json"
    get_movies_file = "/app/landing/movies/*.json"

    # read user data
    df_user = (
        spark.read.format("json")
        .option("inferSchema", "true")
        .option("header", "true")
        .json(get_users_file)
    )

    # read subscription data
    df_subscription = (
        spark.read.format("json")
        .option("inferSchema", "true")
        .option("header", "true")
        .json(get_subscription_file)
    )

    # read credit card data
    df_credit_card = (
        spark.read.format("json")
        .option("inferSchema", "true")
        .option("header", "true")
        .json(get_credit_card_file)
    )

    # read movies data
    df_movies = (
        spark.read.format("json")
        .option("inferSchema", "true")
        .option("header", "true")
        .json(get_movies_file)
    )

    # print schema of dataframe
    df_user.printSchema()
    df_subscription.printSchema()
    df_credit_card.printSchema()
    df_movies.printSchema()

    # write into parquet file on bronze zone
    # file to be available for virtualization engine
    # using minio as storage inside of [k8s]
    df_user.write.format("delta").mode("overwrite").save("s3a://bronze/user/")
    df_subscription.write.format("delta").mode("overwrite").save(
        "s3a://bronze/subscription/"
    )
    df_credit_card.write.format("delta").mode("overwrite").save(
        "s3a://bronze/credit_card/"
    )
    df_movies.write.format("delta").mode("overwrite").save("s3a://bronze/movies/")

    # stop session
    spark.stop()