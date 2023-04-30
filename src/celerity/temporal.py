from datetime import datetime, timezone


def get_julian_date(date: datetime) -> float:
    """
    The Julian date (JD) of any instant is the Julian day number
    plus the fraction of a day since the preceding noon in Universal
    Time (UT).

    :param date: The datetime object to convert.
    :return: The Julian Date (JD) of the given date normalised to UTC.
    """
    return (
        int(
            (
                date.astimezone(tz=timezone.utc)
                - datetime(1970, 1, 1).astimezone(tz=timezone.utc)
            ).total_seconds()
            * 1000
        )
        / 86400000.0
    ) + 2440587.5
