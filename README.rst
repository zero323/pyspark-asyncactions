pyspark-asyncactions
====================

|Build Status| |PyPI version| |Conda Forge version|

A proof of concept asynchronous actions for PySpark using
`concurent.futures <https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures>`__.
Originally developed as proof-of-concept solution for
`SPARK-20347 <https://issues.apache.org/jira/browse/SPARK-20347>`__.

How does it work?
-----------------

The package patches `RDD <https://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.RDD>`__,
`Estimator <https://spark.apache.org/docs/latest/api/python/pyspark.ml.html#pyspark.ml.Estimator>`__,
`DataFrame <https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrame>`__ and
`DataFrameWriter <https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameWriter>`__
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

All ``*Async`` methods return `concurrent.futures.Future <https://docs.python.org/3/library/concurrent.futures.html#future-objects>`__:

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

The package is available on `PyPI <https://pypi.org/project/pyspark-asyncactions>`_:

.. code:: bash

    pip install pyspark-asyncactions
    
and `conda-forge <https://anaconda.org/conda-forge/pyspark-asyncactions>`_:

.. code:: bash

    conda install -c conda-forge pyspark-asyncactions

Installation is required only on the driver node.


Dependencies
------------

The package supports Python 3.6 or later and requires no external dependencies.


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

FAQ
---

- **Why would I need that? Processing in Spark is already distributed.**

  As explained in the `Job Scheduling documentation`_

    (...) within each Spark application, multiple “jobs” (Spark actions) may be running concurrently if they were submitted by different threads.

  However all PySpark actions are blocking. This means that, even if there are free resources on the cluster, each jobs will be executed sequentially
  (paraphrasing `XKCD <https://www.xkcd.com/303/>`__, I am not slacking off, just fitting a ``Pipeline``).

  It is perfectly possible `to achieve the same result using threads <https://stackoverflow.com/q/38048068/1560062>`__ or ``concurrent.futures``
  directly, but the resulting code but resulting can be quite verbose, especially when used in an interactive environment.
  The goal of this package is to make this process as streamlined as possible by hiding all the details (creating and stopping thread pool, job submission).

- **What about** `GIL`_?

  The goal of the package is to enable non-blocking submission of jobs (see above) while the actual processing is handled by the Spark cluster.
  Since heavy lifting is performed by JVM or Python workers as standalone processes, interpreter lock is of lesser concern.

  Because final merging process is applied on the driver, GIL might affect jobs  depending heavily on computationally expensive ``Accumulators`` or reduce-like
  (``reduce``, ``fold``, ``aggregate``) jobs with computationally expensive function.
  The latter problem can be partially addressed using `treeReduce`_.


- **Why not merge this into PySpark?**

  **TL;DR** There was not enough consensus if the feature is essential enough,
  and if it is, what implementation should be used (piggyback onto JVM `AsyncRDDActions`_ vs. native Python implementation).
  For details see `corresponding PR <https://github.com/apache/spark/pull/18052>`_.

  Keeping a separate package gives more freedom (we can add a number of methods not present in the Scala API)
  and better integration with plain Python code, at expense of some more advanced features
  (most notably support for canceling running Spark jobs).

- **When not to use this package?**

  This package is intended primarily to achieve small scale concurrent job execution
  when working with interactive environments. While theoretically it should be possible
  to use it to submit hundreds of independent jobs, it will is likely to stress driver process
  and Py4j gateway and crash the application.

  Therefore I strongly recommend against using it as substitute for a workflow management software.

- **Is this package actively maintained?**

  In general, it has been designed to be as lean as possible, and piggyback on top of standard library, and allow users to add necessary wrappers when needed. Hence, it is pretty much maintenance free and seen almost no activity since its initial release.

  Nonetheless, I consider it actively maintained, and please open an issue if you experience any problems or have feature (like new built-in wrappers) request.

Disclaimer
----------

Apache Spark, Spark, PySpark, Apache, and the Spark logo are `trademarks <https://www.apache.org/foundation/marks/>`__ of `The
Apache Software Foundation <http://www.apache.org/>`__. This project is not owned, endorsed, or
sponsored by The Apache Software Foundation.

.. |Build Status| image:: https://github.com/zero323/pyspark-asyncactions/actions/workflows/test.yml/badge.svg
   :target: https://github.com/zero323/pyspark-asyncactions/actions/workflows/test.yml
.. |PyPI version| image:: https://img.shields.io/pypi/v/pyspark-asyncactions?color=blue
   :target: https://badge.fury.io/py/pyspark-asyncactions
.. |Conda Forge version| image:: https://img.shields.io/conda/vn/conda-forge/pyspark-asyncactions.svg
   :target: https://anaconda.org/conda-forge/pyspark-asyncactions
.. _Job Scheduling documentation: https://spark.apache.org/docs/latest/job-scheduling.html#overview
.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _AsyncRDDActions: https://spark.apache.org/docs/latest/api/scala/index.html#org.apache.spark.rdd.AsyncRDDActions
.. _treeReduce: https://stackoverflow.com/q/32281417/1560062

