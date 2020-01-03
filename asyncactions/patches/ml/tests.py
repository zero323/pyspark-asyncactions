import unittest

from pyspark.tests import ReusedPySparkTestCase  # type: ignore
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, StringIndexerModel

import asyncactions


class AsyncEstimatorActionsTestCase(ReusedPySparkTestCase):
    @classmethod
    def setUpClass(cls):
        ReusedPySparkTestCase.setUpClass()
        cls.spark = SparkSession(cls.sc)

    @classmethod
    def tearDownClass(cls):
        ReusedPySparkTestCase.tearDownClass()
        cls.spark.stop()

    def test_fit_async(self):
        df = self.spark.createDataFrame(["a", "a", "a", "b", "b", "c"], "string")
        indexer = StringIndexer(inputCol="value", outputCol="label")
        f = indexer.fitAsync(df)
        model = f.result()
        self.assertIsInstance(model, StringIndexerModel)
