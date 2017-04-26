from pyspark.rdd import RDD
from asyncactions.utils import patch_all


actions = {
    "collect": ("""
        .. note:: Experimental

        Returns a `concurrent.futures.Future` for retrieving all elements of this RDD.

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.collectAsync()           # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        .. versionadded:: 2.3.0
        """),
    "count": ("""
        .. note:: Experimental

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.countAsync()             # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        10
        """),
    "foreach": (""""
        .. note:: Experimental

        Asynchronously applies a function f to all elements of this RDD
        and returns a `concurrent.futures.Future` of this action.

        >>> def g(x): print(x)               # doctest: +SKIP
        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.foreachAsync(g)          # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        True

        .. versionadded:: 2.3.0
        """),
    "foreachPartition": ("""
        .. note:: Experimental

        Asynchronously applies a function f to each partition of this RDD
        and returns a `concurrent.futures.Future` of this action.

        >>> def g(xs):                       # doctest: +SKIP
        ...     for x in xs:
        ...         print(x)
        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.foreachPartitionAsync(g) # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        .. versionadded:: 2.3.0
        """),
    "take": ("""
        .. note:: Experimental

        Returns a `concurrent.futures.Future` for retrieving
        the first num elements of the RDD.

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.takeAsync(3)             # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        [0, 1, 2]

        .. versionadded:: 2.3.0
        """)
}

patch_all(RDD, actions)
