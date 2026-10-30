[![Celerity](https://github.com/michealroberts/celerity/raw/main/.github/assets/banner.png)](https://celerity.observerly.com)

Celerity is a lightweight, research-grade, zero-dependency type-safe Python library for astronomical calculations to plan your observations. It's only dependency is the Python 3.11+ standard library.

It has been designed to be independent of any other popular astronomical libraries, with a focus on providing a simple and intuitive API for performing common astronomical calculations.

**N.B.** _This project is currently in the early stages of development and is not yet ready for production use._

---

## Usage

### Installation

Celerity can be installed using `uv`:

```console
uv add celerity
```

or `pip`:

```console
pip install celerity
```

or `poetry`:

```console
poetry add celerity
```

### API

The API has been designed to be written in an idiomatic and natural way for English speakers, as well as idiomatic to Python. 

It has been specifically designed to only depend on the core set of Python modules, such that it is not strictly dependent on other popular astronomical libraries, e.g., astropy (although it can compliment the usage of these libraries).

It's important to note that the API does not perform string parsing of times and coordinates, but instead requires the user to provide the correct data types. This is to ensure that the API is type-safe and that the user is aware of the data types being used at all times.

For example, to find out the horizontal coordinate for the star Betelgeuse on the 14th May 2021 at 12:00 UTC, at Mauna Kea, Hawaii, you would write:

```python
from datetime import datetime, timezone

from celerity import Observer, Time

# Mauna Kea, Hawaii:
observer = Observer(
    latitude=19.82,
    longitude=-155.47,
    elevation=4205,
)

# Time of observation in UTC:
time = Time(
    when=datetime(2021, 5, 14, 12, 0, 0, tzinfo=timezone.utc)
)

# Provide an equatorial target in equatorial coordinates at epoch J2000 in units of degrees:
betelgeuse = { ra: 88.792938, dec: 7.407064 }

# Observe the target:
betelgeuse = observer.at(time).observe({ ra: 88.792938, dec: 7.407064 })

# Get the horizontal coordinates:
{ alt, az } = betelgeuse.altAz()

# What is the Local Sidereal Time at the time of observation?
lst = observer.at(time).LST()

# What is the Julian Date at the time of observation?
jd = observer.at(time).JD()
```

### Notes & Caveats

Celerity is designed such that fundamental SI units of measurement are used, e.g., degrees, metres, seconds, etc. This is to ensure that the API is as accurate as possible, and that the user is aware of the units being used at all times.

The `Observer` class requires the user to provide the latitude and longitude in degrees, and the elevation in metres. Latitude is positive for the northern hemisphere, and negative for the southern hemisphere between -90° at the southern pole and +90° at the northern pole. Longitude is always positive for the eastern hemisphere (east of the Prime Meridian), and negative for the western hemisphere (west of the Prime Meridian) representing a longitude between -180° and +180°.

The `Time` class requires the user to provide the time in UTC, and not in any other timezone. The user can, once the `Time` object has been created, convert the time to any other timezone using the provided class methods.

The `Target` class requires the user to provide the right ascension and declination in degrees (and not in hours and degrees).

### Accuracy & ERFA Conformance

The apparent place of a target is derived from its ICRS coordinate using the IAU standard models, evaluated in Terrestrial Time (TT):

- the IAU 2000 frame bias between the ICRS and the mean equator and equinox of J2000.0,
- the IAU 2006 (P03) precession,
- the IAU 2000B nutation, being the 77 largest luni-solar terms of IAU 2000A,
- the gravitational deflection of light by the Sun,
- the relativistic annual aberration, using the Earth's heliocentric velocity from VSOP87.

The frame bias, precession and nutation are composed as rotation matrices and applied to the unit vector of the target, so that the chain remains well conditioned close to the celestial poles.

Celerity is checked against [ERFA](https://github.com/liberfa/erfa), the Essential Routines for Fundamental Astronomy derived from the IAU SOFA library, in `tests/test_conformance_erfa.py`. The reference values are evaluated once with `pyerfa` and stored in the test as literals, so that the test suite carries no dependency on ERFA. Each quantity is compared over a grid of dates between 2000 and 2040 and targets spanning both hemispheres, including a target within a degree of the celestial pole, and must agree with ERFA to within a stated tolerance on the sky. The tolerances are tightened as the models improve and are never loosened.

The current worst-case differences from ERFA over that grid, in milliarcseconds, are:

| Quantity                              | Difference | Tolerance |
| ------------------------------------- | ---------: | --------: |
| Precession                            |     0.0002 |         1 |
| Nutation                              |        0.7 |         2 |
| Light deflection                      |     0.0001 |       0.1 |
| Annual aberration                     |       0.07 |       0.5 |
| Apparent place                        |       10.4 |        12 |

**N.B.** _The nutation difference is the truncation of the IAU 2000B series relative to IAU 2000A._

**N.B.** _The apparent place difference is the barycentric motion of the Sun, which VSOP87 does not supply._

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
