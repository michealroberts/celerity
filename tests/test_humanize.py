from src.celerity.humanize import format_degree_as_dms, format_degree_as_hms


def test_format_degree_as_dms():
    humanised = format_degree_as_dms(-11.1614)
    assert humanised == "-11° 09' 41.04\""
    humanised = format_degree_as_dms(7.4070639)
    assert humanised == "+07° 24' 25.43\""


def test_format_degree_as_hms():
    humanised = format_degree_as_hms(88.7929583)
    assert humanised == "05h 55m 10.31s"
    humanised = format_degree_as_hms(-88.7929583)
    assert humanised == "18h 04m 49.69s"
