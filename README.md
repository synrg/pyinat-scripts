Miscellaneous scripts using pyinaturalist.

# Installation

- [Install uv](install-uv)
- Clone this repo:
```sh
$ git clone https://github.com/synrg/pyinat-scripts
```

# Usage

- Run each script with uv, e.g.
```sh
$ cd pyinat-scripts
$ uv run faves dgcurrywheel place_id=7095
```
- By default, scripts run against the `main` branch of pyinaturalist from
  github, as some of them only work with that version.
- To use another version, specify `--with` to override the dependency, e.g.
```sh
$ uv run --with pyinaturalist==0.20 test_subtree_and_rank_filter.py
```

## Install uv

Follow the instructions at https://docs.astral.sh/uv/getting-started/installation/
to install `uv` for your operating system.
