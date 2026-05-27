import os

import pytest


@pytest.fixture
def dask_env():
    from distributed import LocalCluster, Client, Variable
    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=False)
    client = Client(cluster)
    Variable("workers", client=client).set([w_addr for w_addr in client.scheduler_info()["workers"].keys()])
    yield client, cluster
    # teardown
    client.close()
    cluster.close()


@pytest.fixture
def ray_env():  # TODO: replace dask with ray
    from distributed import LocalCluster, Client, Variable
    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=False)
    client = Client(cluster)
    Variable("workers", client=client).set([w_addr for w_addr in client.scheduler_info()["workers"].keys()])
    yield client, cluster
    # teardown
    client.close()
    cluster.close()
