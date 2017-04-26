import textwrap
from pyspark.context import SparkContext
from pyspark.rdd import RDD
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.readwriter import DataFrameWriter


def get_context(x):
    if isinstance(x, RDD):
        return x.ctx
    if isinstance(x, DataFrame):
        return x._sc
    if isinstance(x, DataFrameWriter):
        return x._spark._sc


def async_action(f):
    def async_action_(self, *args, **kwargs):
        executor = get_context(self)._get_executor()
        return executor.submit(f, self, *args, **kwargs)
    return async_action_


def patch_async(cls, method, doc, suffix):
    f = async_action(getattr(cls, method))
    f.__doc__ = textwrap.dedent(doc)
    setattr(cls, "{}{}".format(method, suffix), f)


def patch_all(cls, mapping, suffix="Async"):
    for method, doc in mapping.items():
        patch_async(cls, method, doc, suffix)