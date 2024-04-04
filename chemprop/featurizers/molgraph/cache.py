from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, Iterable

import numpy as np

from chemprop.featurizers.molgraph.base import MolGraphFeaturizer, T
from chemprop.featurizers.molgraph.molgraph import MolGraph


class MolGraphCacheFacade(Sequence[MolGraph], Generic[T]):
    """
    A :class:`MolGraphCacheFacade` provided an interface for caching
    :class:`~chemprop.featurizers.molgraph.molgraph.MolGraph`\s.

    .. note::
        This class only provides a facade for a cached dataset, but it does **not** guarantee
        whether the underlying data is truly cached.


    Parameters
    ----------
    inputs : Iterable[T]
        The inputs to be featurized.
    V_fs : Iterable[np.ndarray]
        The node features for each input.
    E_fs : Iterable[np.ndarray]
        The edge features for each input.
    featurizer : MolGraphFeaturizer[T]
        The featurizer with which to generate the
        :class:`~chemprop.featurizers.molgraph.molgraph.MolGraph`\s.
    """

    @abstractmethod
    def __init__(
        self,
        inputs: Iterable[T],
        V_fs: Iterable[np.ndarray],
        E_fs: Iterable[np.ndarray],
        featurizer: MolGraphFeaturizer[T],
    ):
        pass


class MolGraphCache(MolGraphCacheFacade):
    """
    A :class:`MolGraphCache` precomputes the corresponding
    :class:`~chemprop.featurizers.molgraph.molgraph.MolGraph`\s and caches them in memory.
    """

    def __init__(
        self,
        inputs: Iterable[T],
        V_fs: Iterable[np.ndarray | None],
        E_fs: Iterable[np.ndarray | None],
        featurizer: MolGraphFeaturizer[T],
    ):
        self._mgs = [featurizer(input, V_f, E_f) for input, V_f, E_f in zip(inputs, V_fs, E_fs)]

    def __len__(self) -> int:
        return len(self._mgs)

    def __getitem__(self, index: int) -> MolGraph:
        return self._mgs[index]


class MolGraphCacheOnTheFly(MolGraphCacheFacade):
    """
    A :class:`MolGraphCacheOnTheFly` computes the corresponding
    :class:`~chemprop.featurizers.molgraph.molgraph.MolGraph`\s as they are requested.
    """

    def __init__(
        self,
        inputs: Iterable[T],
        V_fs: Iterable[np.ndarray | None],
        E_fs: Iterable[np.ndarray | None],
        featurizer: MolGraphFeaturizer[T],
    ):
        self._inputs = list(inputs)
        self._V_fs = list(V_fs)
        self._E_fs = list(E_fs)
        self._featurizer = featurizer

    def __len__(self) -> int:
        return len(self._inputs)

    def __getitem__(self, index: int) -> MolGraph:
        return self._featurizer(self._inputs[index], self._V_fs[index], self._E_fs[index])
