# DEISA

**DEISA** is a **meta-package** for the DEISA ecosystem (Dask Enabled In-Situ Analysis).

This repository does **not** contain backend implementations itself. Instead, it provides a convenient entry point that:
- Installs the supported DEISA backends ([Dask](https://deisa-project/deisa-dask) and [Ray]((https://deisa-project/deisa-ray))
- Ensures **API compliance** across backends via a shared test suite
- Validates that each backend correctly implements the DEISA core interfaces


## What this package provides
Installing `deisa` pulls in:
- `deisa-core` – shared interfaces and abstractions
- `deisa-dask` – Dask backend implementation
- `deisa-ray` – Ray backend implementation


## Installation
Install the full DEISA stack (all supported backends):

```bash
pip install deisa
```

Backend-specific installs are available if you only need one runtime:

```bash
pip install deisa[dask]
pip install deisa[ray]
```


## API compliance testing
This repository hosts API compliance tests that are executed against each backend to ensure:
- Consistent behavior across runtimes
- Conformance to the DEISA core API
- Early detection of backend regressions

Backend implementations are expected to pass this test suite unchanged.


## Project links

- Source: https://github.com/deisa-project/deisa
- Issues: https://github.com/deisa-project/deisa/issues

## Acknowledgement
As part of the "France 2030" initiative, this work has benefited from a State grant managed by the French National Research Agency (Agence Nationale de la Recherche) attributed to the Exa-DoST project of the NumPEx PEPR program, reference: ANR-22-EXNU-0004.

