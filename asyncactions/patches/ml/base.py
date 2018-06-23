from pyspark.ml.base import Estimator
from asyncactions.utils import patch_all

actions = {
    "fit": """Asynchronously fits a model to the input dataset with optional parameters.

        :param dataset: input dataset, which is an instance of :py:class:`pyspark.sql.DataFrame`
        :param params: an optional param map that overrides embedded params. If a list/tuple of
                       param maps is given, this calls fit on each param map and returns a list of
                       models.
        :returns: :py:class:`concurrent.futures.Future` of fitted model(s)
        """
}

patch_all(Estimator, actions)
