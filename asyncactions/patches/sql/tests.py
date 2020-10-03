import tempfile
import shutil
import os
import unittest

from sparktestingbase.testcase import SparkTestingBaseReuse  # type: ignore
from pyspark.sql import SparkSession
from pyspark.sql.types import Row

import asyncactions


class AsyncDataFrameActionsTestCase(SparkTestingBaseReuse):
    @classmethod
    def setUpClass(cls):
        SparkTestingBaseReuse.setUpClass()
        cls.spark = SparkSession(cls.sc)

    @classmethod
    def tearDownClass(cls):
        SparkTestingBaseReuse.tearDownClass()
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
        self.assertTrue(f.result() is None and acc1.value == len(data))

        acc2 = self.sc.accumulator(0)
        f = df.foreachPartitionAsync(lambda xs: [acc2.add(1) for _ in xs])
        self.assertTrue(f.result() is None and acc2.value == len(data))


class AsyncDataFrameWriterActionsTestCase(SparkTestingBaseReuse):
    @classmethod
    def setUpClass(cls):
        SparkTestingBaseReuse.setUpClass()
        cls.spark = SparkSession(cls.sc)
        cls.tempdir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        SparkTestingBaseReuse.tearDownClass()
        cls.spark.stop()
        shutil.rmtree(cls.tempdir)

    def test_save_async(self):
        data = [Row(id=i) for i in range(10)]
        df = self.spark.createDataFrame(data)

        path = os.path.join(self.tempdir, "saved_async")
        f = df.write.format("json").saveAsync(path)

        self.assertIsNone(f.result())
        loaded = self.spark.read.format("json").load(path)
        self.assertEqual(loaded.count(), 10)
        self.assertEqual(sorted(loaded.collect()), data)


if __name__ == "__main__":
    unittest.main()
