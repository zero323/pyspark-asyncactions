import unittest
from pyspark.tests import ReusedPySparkTestCase
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
import asyncactions


class AsyncRDDActionsTestCase(ReusedPySparkTestCase):
    def test_async_actions(self):
        data = [x for x in range(10)]
        rdd = self.sc.parallelize(data)
        f = rdd.collectAsync()
        self.assertListEqual(f.result(), data)

        f = rdd.countAsync()
        self.assertEqual(f.result(), 10)

        f = rdd.takeAsync(5)
        self.assertEqual(f.result(), data[:5])

        acc1 = self.sc.accumulator(0)

        f = rdd.foreachAsync(lambda _: acc1.add(1))
        self.assertTrue(
            f.result() is None and acc1.value == len(data)
        )

        acc2 = self.sc.accumulator(0)
        f = rdd.foreachPartitionAsync(lambda xs: [acc2.add(1) for _ in xs])
        self.assertTrue(
            f.result() is None and acc2.value == len(data)
        )


class AsyncDataFrameActionsTestCase(ReusedPySparkTestCase):
    @classmethod
    def setUpClass(cls):
        ReusedPySparkTestCase.setUpClass()
        cls.spark = SparkSession(cls.sc)

    @classmethod
    def tearDownClass(cls):
        ReusedPySparkTestCase.tearDownClass()
        cls.spark.stop()

    def test_async_actions(self):
        data = [Row(id=i) for i in range(10)]
        df = self.spark.createDataFrame(data)
        f = df.collectAsync()
        self.assertListEqual(f.result(), data)

        f = df.countAsync()
        self.assertEqual(f.result(), 10)

        f = df.takeAsync(3)
        self.assertEqual(f.result(), data[:3])

        acc1 = self.sc.accumulator(0)

        f = df.foreachAsync(lambda _: acc1.add(1))
        self.assertTrue(
            f.result() is None and acc1.value == len(data)
        )

        acc2 = self.sc.accumulator(0)
        f = df.foreachPartitionAsync(lambda xs: [acc2.add(1) for _ in xs])
        self.assertTrue(
            f.result() is None and acc2.value == len(data)
        )


if __name__ == '__main__':
    unittest.main()
