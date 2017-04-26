import concurrent.futures
from pyspark.context import SparkContext


def _get_executor(self):
    """ Return existing thread pool executor
    or create a new one.
    """
    # This would fail anyway, but
    # we don't want an orphan executor
    if SparkContext._active_spark_context is None:
        raise ValueError("No active SparkContext")

    if getattr(SparkContext, "_thread_pool_executor", None) is None:
        try:
            import concurrent.futures

            # Make sure that there is only one executor
            with SparkContext._lock:
                cores = self.getConf().get("spark.driver.cores") or 2
                # In case of another thread got lock first
                SparkContext._thread_pool_executor = (
                    getattr(SparkContext, "_thread_pool_executor", None) or
                    concurrent.futures.ThreadPoolExecutor(max_workers=cores)
                )

        # Python 2.7 and not futures backport installed
        except ImportError as e:
            msg = "{}. Async actions require Python >= 3.2 or futures package installed"
            raise ImportError(msg.format(e.message))

    return SparkContext._thread_pool_executor


SparkContext._get_executor = _get_executor
