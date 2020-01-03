from pyspark.rdd import RDD
from asyncactions.utils import patch_all


actions = {
    "collect": (
        """Returns a :py:class:`concurrent.futures.Future` for retrieving all elements of this RDD.

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.collectAsync()           # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
    ),
    "count": (
        """Return :py:class:`concurrent.futures.Future` of the number of elements in this RDD.

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.countAsync()             # doctest: +SKIP
        >>> f.result()                       # doctest: +SKIP
        10
        """
    ),
    "foreach": (
        """Asynchronously applies a function f to all elements of this RDD
        and returns a :py:class:`concurrent.futures.Future` of this action.

        >>> def g(x): print(x)               # doctest: +SKIP
        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.foreachAsync(g)          # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        True
        """
    ),
    "foreachPartition": (
        """Asynchronously applies a function f to each partition of this RDD
        and returns a :py:class:`concurrent.futures.Future` of this action.

        >>> def g(xs):                       # doctest: +SKIP
        ...     for x in xs:
        ...         print(x)
        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.foreachPartitionAsync(g) # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        """
    ),
    "take": (
        """Returns a :py:class:`concurrent.futures.Future` for retrieving
        the first num elements of the RDD.

        >>> rdd = sc.parallelize(range(10))  # doctest: +SKIP
        >>> f = rdd.takeAsync(3)             # doctest: +SKIP
        >>> f.result() is None               # doctest: +SKIP
        [0, 1, 2]
        """
    ),
    "saveAsTextFile": (
        """Asynchronously save this RDD as a text file, using string representations of elements
        and returns :py:class:`concurrent.futures.Future` of this action.

        :param path: path to text file
        :param compressionCodecClass: (None by default) string i.e. "org.apache.hadoop.io.compress.GzipCodec"
        """
    ),
}

patch_all(RDD, actions)
