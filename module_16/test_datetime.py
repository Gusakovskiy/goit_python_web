

from freezegun import freeze_time
import datetime


def right_time():
    return datetime.datetime.now().year == 2019


@freeze_time("2019-01-14")
def test_2019():
    assert right_time() is True

import pdb; pdb.set_trace()