asyncactions
============

|Build Status| |PyPI version|

A proof of concept asynchronous actions for PySpark using
`concurent.futures <https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures>`__
Originally developed as proof-of-concept solution for
`SPARK-20347 <https://issues.apache.org/jira/browse/SPARK-20347>`__

How does it work?
-----------------

The package patches ``RDD``, ``DataFrame`` and ``DataFrameWriter``
classes by adding thin wrappers to the commonly used action methods.

Methods are patched by retrieving shared
`ThreadPoolExecutor <https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor>`__
(attached to ``SparkContext``) and applying its ``submit`` method:

.. code:: python

    def async_action(f):
        def async_action_(self, *args, **kwargs):
            executor = get_context(self)._get_executor()
            return executor.submit(f, self, *args, **kwargs)
        return async_action_

The naming convention for the patched methods is ``methodNameAsync``,
for example:

-  ``RDD.count`` ⇒ ``RDD.countAsync``
-  ``DataFrame.take`` ⇒ ``RDD.takeAsync``
-  ``DataFrameWriter.save`` ⇒ ``DataFrameWriter.saveAsync``

Number of threads is determined as follows:

-  ``spark.driver.cores`` if is set.
-  2 otherwise.

Usage
-----

To patch existing classes just import the package:

.. code:: python

    >>> import asyncactions
    >>> from pyspark.sql import SparkSession
    >>>
    >>> spark = SparkSession.builder.getOrCreate()

All ``*Async`` methods return ``concurrent.futures._base.Future``:

.. code:: python

    >>> rdd = spark.sparkContext.range(100)
    >>> f = rdd.countAsync()
    >>> f
    <Future at ... state=running>
    >>> type(f)
    concurrent.futures._base.Future
    >>> f.add_done_callback(lambda f: print(f.result()))
    100


and the result can be used whenever ``Future`` is expected.

Installation
------------

The package is available on PYPI:

.. code:: bash

    pip install pyspark-asyncactions

Installation is required only on the driver node.

Do it yourself
--------------

Define actions dictionary which maps from the method name to the docstring:

.. code:: python

    >>> actions = {"evaluate": """Asynchronously evaluates the output with optional parameters.
    ...         :param dataset: a dataset that contains labels/observations and
    ...                         predictions
    ...         :param params: an optional param map that overrides embedded
    ...                        params
    ...         :return: :py:class:`concurrent.futures.Future` of metric
    ...         """}

Call asyncactions.utils.patch_all method with class and actions as the arguments

.. code:: Python

    >>> import asyncactions.utils
    >>> from pyspark.ml.evaluation import Evaluator, RegressionEvaluator
    >>> asyncactions.utils.patch_all(Evaluator, actions)

Enjoy your new asynchronous method

.. code:: python

    >>> import asyncactions
    >>> df = spark.createDataFrame([(1.0, 1.0), (1.0, -1.0), (0.0, 1.0)], ("label", "prediction"))
    >>> metrics = RegressionEvaluator().evaluateAsync(df)
    >>> metrics.result()  # Note that result is blocking
    1.2909944487358058


Dependencies
------------

The package supports Python 3.5 or later with a common codebase and
requires no external dependencies.

It is also possible, but not supported, to use it with Python 2.7, using
`concurent.futures backport <https://pypi.org/project/futures/>`__.

Disclaimer
----------

Apache Spark, Spark, PySpark, Apache, and the Spark logo are `trademarks <https://www.apache.org/foundation/marks/>`__ of `The
Apache Software Foundation <http://www.apache.org/>`__. This project is not owned, endorsed, or
sponsored by The Apache Software Foundation.

.. |Build Status| image:: https://travis-ci.org/zero323/pyspark-asyncactions.svg?branch=master
   :target: https://travis-ci.org/zero323/pyspark-asyncactions
.. |PyPI version| image:: https://badge.fury.io/py/pyspark-asyncactions.svg
   :target: https://badge.fury.io/py/pyspark-asyncactions
