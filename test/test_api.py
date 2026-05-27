import importlib

import pytest
from deisa.core import IDeisa, IBridge

from common import dask_env, ray_env

module_name = {
    dask_env.__name__: "deisa.dask",
    ray_env.__name__: "deisa.dask",  # TODO change to deisa.ray
}


@pytest.mark.parametrize("env_setup", [dask_env.__name__, ray_env.__name__])
def test_deisa_api(request, env_setup):
    client, cluster = request.getfixturevalue(env_setup)
    module = importlib.import_module(module_name[env_setup])
    deisa: IDeisa = module.Deisa(wait_for_go=False)
    assert isinstance(deisa, IDeisa)


@pytest.mark.parametrize("env_setup", [dask_env.__name__, ray_env.__name__])
def test_bridge_api(request, env_setup):
    from mpi4py import MPI
    client, cluster = request.getfixturevalue(env_setup)
    module = importlib.import_module(module_name[env_setup])
    bridge: IBridge = module.Bridge(MPI.COMM_WORLD,
                                    arrays_metadata={
                                        'temperature': {
                                            'global_shape': (8, 8),
                                            'chunk_shape': (8, 8),
                                            'chunk_position': (0, 0)
                                        },
                                    },
                                    wait_for_go=False)
    assert isinstance(bridge, IBridge)
