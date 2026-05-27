import os

import pytest


@pytest.fixture
def dask_env():
    from distributed import LocalCluster, Client
    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=True,
                           dashboard_address=":0", worker_dashboard_address=":0")
    os.environ['DEISA_DASK_SCHEDULER_ADDRESS'] = cluster.scheduler_address
    cluster.wait_for_workers(1)
    client = Client(cluster)
    yield client, cluster
    # teardown
    client.close()
    cluster.close()


@pytest.fixture
def ray_env():  # TODO: replace dask with ray
    from distributed import LocalCluster, Client
    cluster = LocalCluster(n_workers=1, threads_per_worker=1, processes=True,
                           dashboard_address=":0", worker_dashboard_address=":0")
    os.environ['DEISA_DASK_SCHEDULER_ADDRESS'] = cluster.scheduler_address
    cluster.wait_for_workers(1)
    client = Client(cluster)
    yield client, cluster
    # teardown
    client.close()
    cluster.close()
