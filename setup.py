from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


dask_deps = [
    "dask",
    "distributed",
    "numpy",
    "deisa-dask==0.3.0",
]

ray_deps = [
    "ray",
    # "deisa-ray==x.y.z",   # TODO
]

test_deps = [
    "pytest",
    "mypy",
    "deisa-core==0.1.0",
    *dask_deps,
    *ray_deps,
]

setup(name='deisa',
      version="0.3.0",
      description='Dask enabled in-situ analysis',
      long_description=readme(),
      long_description_content_type='text/markdown',
      license='MIT',
      url='https://github.com/deisa-project/deisa',
      project_urls={
          'Bug Reports': 'https://github.com/deisa-project/deisa/issues',
          'Source': 'https://github.com/deisa-project/deisa',
      },
      author='Benoît Martin',
      author_email='bmartin@cea.fr',
      python_requires='>=3.8',
      keywords='deisa in-situ',
      install_requires=[*dask_deps, *ray_deps],  # by default, include all backends,
      extras_require={
          "dask": dask_deps,
          "ray": ray_deps,
          "test": test_deps,
      },
      classifiers=[
          "Programming Language :: Python :: 3.8",
          "Operating System :: OS Independent",
          "Development Status :: 3 - Alpha"
      ]
      )
