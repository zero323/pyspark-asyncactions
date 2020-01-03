from functools import update_wrapper

from pyspark.context import SparkContext
from pyspark.rdd import RDD
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.readwriter import DataFrameWriter


def get_context(self) -> SparkContext:
    return SparkContext._active_spark_context  # type: ignore [attr-defined]


def async_action(f):
    def async_action_(self, *args, **kwargs):
        executor = get_context(self)._get_executor()
        return executor.submit(f, self, *args, **kwargs)

    return async_action_


def patch_async(cls, method, doc, suffix):
    g = getattr(cls, method)
    f = update_wrapper(
        async_action(g),
        g,
        assigned=["__module__", "__annotations__"]
        if hasattr(g, "__annotations__")
        else ["__module__"],
    )
    f.__doc__ = doc
    setattr(cls, "{}{}".format(method, suffix), f)


def patch_all(cls, mapping, suffix: str = "Async"):
    for method, doc in mapping.items():
        patch_async(cls, method, doc, suffix)
