# **************************************************************************************

# @author         Michael Roberts <michael@observerly.com>
# @package        @observerly/celerity
# @license        Copyright © 2021-2026 observerly

# **************************************************************************************

from typing import get_args

from src.celerity.matrix import Matrix

# **************************************************************************************


def test_matrix_has_three_rows():
    assert len(get_args(Matrix)) == 3


# **************************************************************************************


def test_matrix_rows_have_three_float_components():
    for row in get_args(Matrix):
        assert get_args(row) == (float, float, float)


# **************************************************************************************


def test_matrix_accepts_a_three_by_three_tuple():
    identity: Matrix = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    assert len(identity) == 3
    assert all(len(row) == 3 for row in identity)


# **************************************************************************************
