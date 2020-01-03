import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor

from pyspark.context import SparkContext


def _get_executor(self: SparkContext) -> ThreadPoolExecutor:
    """ Return existing thread pool executor
    or create a new one.
    """
    # This would fail anyway, but
    # we don't want an orphan executor
    if SparkContext._active_spark_context is None:  # type: ignore [attr-defined]
        raise ValueError("No active SparkContext")

    if getattr(SparkContext, "_thread_pool_executor", None) is None:
        import concurrent.futures

        # Make sure that there is only one executor
        with SparkContext._lock:  # type: ignore [attr-defined]
            cores = int(self.getConf().get("spark.driver.cores") or 2)
            # In case of another thread got lock first
            SparkContext._thread_pool_executor = getattr(  # type: ignore [attr-defined]
                SparkContext, "_thread_pool_executor", None
            ) or concurrent.futures.ThreadPoolExecutor(max_workers=cores)

    return SparkContext._thread_pool_executor  # type: ignore [attr-defined]


def stop(self: SparkContext) -> None:
    with SparkContext._lock:  # type: ignore [attr-defined]
        if getattr(SparkContext, "_thread_pool_executor", None):
            SparkContext._thread_pool_executor.shutdown()  # type: ignore [attr-defined]
            SparkContext._thread_pool_executor = None  # type: ignore [attr-defined]
    SparkContext._stop(self)  # type: ignore [attr-defined]


SparkContext._stop = SparkContext.stop  # type: ignore [assignment,attr-defined]
SparkContext.stop = stop  # type: ignore [assignment]
SparkContext._get_executor = _get_executor  # type: ignore [assignment,attr-defined]
