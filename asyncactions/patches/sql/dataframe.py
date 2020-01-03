from pyspark.sql.dataframe import DataFrame
from asyncactions.utils import patch_all


actions = {
    "collect": (
        """Returns a :py:class:`concurrent.futures.Future` for retrieving all elements of this DataFrame.

        >>> df = spark.range(8)             # doctest: +SKIP
        >>> f = df.collectAsync()            # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        [Row(id=0), Row(id=1), Row(id=2), Row(id=3), Row(id=4), Row(id=5), Row(id=6), Row(id=7)]
        """
    ),
    "count": (
        """
        >>> df = spark.range(10)             # doctest: +SKIP
        >>> f = df.countAsync()              # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        10
        """
    ),
    "foreach": (
        """Asynchronously applies a function f to all elements of this DataFrame
        and returns a :py:class:`concurrent.futures.Future` of this action.

        >>> def g(x): print(x)               # doctest: +SKIP
        >>> df = spark.range(10)             # doctest: +SKIP
        >>> f = df.foreachAsync(g)           # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        True
        """
    ),
    "foreachPartition": (
        """Asynchronously applies a function f to each partition of this DataFrame
        and returns a :py:class:`concurrent.futures.Future` of this action.

        >>> def g(xs):                       # doctest: +SKIP
        ...     for x in xs:
        ...         print(x)
        >>> df = spark.range(10)             # doctest: +SKIP
        >>> f = df.foreachPartitionAsync(g)  # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        """
    ),
    "take": (
        """Returns a :py:class:`concurrent.futures.Future` for retrieving
        the first num elements of the DataFrame.

        >>> rdd = spark.range(10)            # doctest: +SKIP
        >>> f = df.takeAsync(3)              # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        [Row(id=0), Row(id=1), Row(id=2)]
        """
    ),
}


patch_all(DataFrame, actions)
