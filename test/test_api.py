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
    deisa: IDeisa = module.Deisa(get_connection_info=lambda: client, wait_for_go=False)

    assert hasattr(deisa, 'close') and callable(deisa.close)
    assert hasattr(deisa, 'get_array') and callable(deisa.get_array)
    assert hasattr(deisa, 'register_sliding_window_callback') and callable(deisa.register_sliding_window_callback)
    assert hasattr(deisa, 'unregister_sliding_window_callback') and callable(deisa.unregister_sliding_window_callback)
    assert hasattr(deisa, "set") and callable(deisa.set)
    assert hasattr(deisa, "delete") and callable(deisa.delete)


@pytest.mark.parametrize("env_setup", [dask_env.__name__, ray_env.__name__])
def test_bridge_api(request, env_setup):
    client, cluster = request.getfixturevalue(env_setup)
    module = importlib.import_module(module_name[env_setup])
    bridge: IBridge = module.Bridge(id=0,
                                    arrays_metadata={},
                                    system_metadata={'connection': client, 'nb_bridges': 1},
                                    wait_for_go=False)

    assert hasattr(bridge, 'send') and callable(bridge.send)
    assert hasattr(bridge, 'get') and callable(bridge.get)
