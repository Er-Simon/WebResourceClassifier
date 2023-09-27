from pyspark.sql import SparkSession
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, VectorAssembler
from nltk.stem.snowball import SnowballStemmer
from pyspark.sql import functions as F
from pyspark.sql.types import *


spark = SparkSession.builder.getOrCreate()
loaded_model = PipelineModel.load("./WebsiteClassificationModel/")
indexToString = {0: 'Adult', 1: 'Arts', 2: 'Business', 3: 'Computers', 4: 'Games', 5: 'Health', 6: 'Home', 7: 'Kids', 8: 'News', 9: 'Recreation', 10: 'Reference', 11: 'Science', 12: 'Shopping', 13: 'Society', 14: 'Sports'}

def clean_text(df, column_name):
    lower_case_news_df = df.withColumn(column_name, F.lower(F.col(column_name)))
    trimmed_news_df = lower_case_news_df.withColumn(column_name, F.trim(F.col(column_name)))
    no_punct_news_df = trimmed_news_df.withColumn(column_name, (F.regexp_replace(F.col(column_name), "[^a-zA-Z\s]", "")))

    cleaned_news_df = no_punct_news_df.withColumn(column_name, F.trim(F.regexp_replace(F.col(column_name), " +", " ")))

    tokenizer = Tokenizer(inputCol=column_name, outputCol="tokens")
    tokens_df = tokenizer.transform(cleaned_news_df)
    
    stopwords_remover = StopWordsRemover(inputCol="tokens", outputCol="terms")
    terms_df = stopwords_remover.transform(tokens_df)

    stemmer = SnowballStemmer(language="english")
    stemmer_udf = F.udf(lambda tokens: [stemmer.stem(token) for token in tokens], ArrayType(StringType()))
    terms_stemmed_df = terms_df.withColumn(f"cleaned_{column_name}", stemmer_udf("terms"))

    return terms_stemmed_df


def classify(title, description):
    response = None

    data = [
        (title, description)
    ]

    new_data_df = spark.createDataFrame(
        data, ["title", "description"])
    
    clean_df_title = clean_text(new_data_df, column_name="title")
    clean_df_title = clean_df_title.select("cleaned_title")

    clean_df_description = clean_text(new_data_df, column_name="description")
    clean_df_description = clean_df_description.select("cleaned_description")

    df = clean_df_title.join(clean_df_description)

    df = df.withColumnRenamed("cleaned_title", "title")
    df = df.withColumnRenamed("cleaned_description", "description")

    predictions = loaded_model.transform(df)

    predictions.show()

    row = predictions.first()

    #print("[INFO] classify\nresponse: {}\n".format(row))

    if row:
        response = indexToString[int(row.prediction)]
    else:
        response = "INTERNAL ERROR"
        print("\n[ERROR classify]\nrequest\ntitle: {}\ndescription: {}\n\nprediction: {}\n".format(title, description, row))

    return response