from pyspark.sql.readwriter import DataFrameWriter
from asyncactions.utils import patch_all


actions = {
    "save": """Asynchronously saves the contents of the :class:`DataFrame` to a data source
        and returns a :py:class:`concurrent.futures.Future` of this action.

        The data source is specified by the ``format`` and a set of ``options``.
        If ``format`` is not specified, the default data source configured by
        ``spark.sql.sources.default`` will be used.

        :param path: the path in a Hadoop supported file system
        :param format: the format used to save
        :param mode: specifies the behavior of the save operation when data already exists.

            * ``append``: Append contents of this :class:`DataFrame` to existing data.
            * ``overwrite``: Overwrite existing data.
            * ``ignore``: Silently ignore this operation if data already exists.
            * ``error`` or ``errorifexists`` (default case): Throw an exception if data already \
                exists.
        :param partitionBy: names of partitioning columns
        :param options: all other string options


        >>> _ = (df.write.mode('append').format("parquet")              # doctest: +SKIP
        ...     .saveAsync(os.path.join(tempfile.mkdtemp(), 'data')))
        """
}


patch_all(DataFrameWriter, actions)
