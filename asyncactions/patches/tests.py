import os
import shutil
import tempfile
import unittest

from sparktestingbase.testcase import SparkTestingBaseReuse  # type: ignore
import asyncactions


class AsyncRDDActionsTestCase(SparkTestingBaseReuse):
    @classmethod
    def setUpClass(cls):
        SparkTestingBaseReuse.setUpClass()
        cls.tempdir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        SparkTestingBaseReuse.tearDownClass()
        shutil.rmtree(cls.tempdir)

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
        self.assertTrue(f.result() is None and acc1.value == len(data))

        acc2 = self.sc.accumulator(0)
        f = rdd.foreachPartitionAsync(lambda xs: [acc2.add(1) for _ in xs])
        self.assertTrue(f.result() is None and acc2.value == len(data))

        path = os.path.join(self.tempdir, "rdd_saved_async")
        f = rdd.saveAsTextFileAsync(path)

        self.assertIsNone(f.result())

        self.assertEqual(
            sorted(self.sc.textFile(path).collect()), [str(x) for x in data]
        )


if __name__ == "__main__":
    unittest.main()
