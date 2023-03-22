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
        SparkSession.builder.appName("transform_and_enrichment_from_bronze_to_silver")
        .config("spark.sql.warehouse.dir", abspath("spark-warehouse"))
        .enableHiveSupport()
        .getOrCreate()
    )

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # set dynamic input file [hard-coded]
    # can be changed for input parameters [spark-submit]
    get_users_file = "s3a://bronze/users/"
    get_subscription_file = "s3a://bronze/subscriptions/"
    get_credit_card_file = "s3a://bronze/credit_cards/"
    get_movies_file = "s3a://bronze/movies/"

    # read user data
    df_bronze_user = spark.read.format("delta").format("delta").load(get_users_file)

    # read subscription data
    df_bronze_subscription = spark.read.format("delta").load(get_subscription_file)

    # read credit card data
    df_bronze_credit_card = spark.read.format("delta").load(get_credit_card_file)

    # read movies data
    df_bronze_movies = spark.read.format("delta").load(get_movies_file)

    select_columns_user = df_bronze_user.select(
        "uid",
        "user_id",
        "first_name",
        "last_name",
        "address.country",
        "employment.title",
        "dt_current_timestamp",
    )

    select_columns_user.show()

    # stop session
    spark.stop()
