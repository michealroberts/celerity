# Celerity

Celerity is a lightweight, zero-dependency and type-safe Python library for astronomical calculations.

---

## Package Development

### Project Requirements

- [Python](https://www.python.org/) 3.11.*
- [Docker](https://www.docker.com/).
- [Docker Compose](https://docs.docker.com/compose/install/).
- [Poetry](https://python-poetry.org/) for Python package and environment management.

### Installing Dependencies

The Celerity project manages Python package dependencies using [Poetry](https://python-poetry.org/). You'll need to follow the instructions for installation there.

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

**N.B.** For development with vscode you will need to run the following command:

```console
$ poetry config virtualenvs.in-project true
```

This will installed the poetry `.venv` in the root of the project and allow vscode to setup the environment correctly for development.

To start development, install all of the dependencies as:

```console
$ poetry install
```

**N.B.** _Ensure that any dependency changes are committed to source control, so everyone has a consistenct package dependecy list._

### Local Development

The Celerity development stack can be built with the following `docker` `compose` command, with the `$INSTALL_DEV` build environment argument\*.

```console
$ docker compose -f local.yml build --build-arg INSTALL_DEV="true"
```

\* _This is required to install the development dependencies in the container._

Then start the development stack with a running shell session with:

```console
$ docker compose -f local.yml run app bash
```

**N.B.** _The `docker compose` command will build the development stack if it has not been built already._

### Running Tests

To run the tests, please ensure you have followed the steps for building the development server:

The Celerity development stack can be built with the following `docker` `compose` command, with the `$INSTALL_DEV` build environment argument\*.

```console
$ docker compose -f local.yml build --build-arg INSTALL_DEV="true"
```

You can then run the pytest suite using the following command:

```
$ docker compose -f local.yml exec api pytest
```