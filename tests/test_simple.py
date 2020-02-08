import os.path

import pytest

import emlx


TEST_FILE = "test.emlx"


@pytest.fixture
def message(request):
    dirname = os.path.dirname(request.module.__file__)
    filepath = f"{dirname}/{TEST_FILE}"
    return emlx.read(filepath)


def test_bytecount(message):
    assert message.bytecount == 545


def test_data(message):
    assert (
        message.data["Message-Id"]
        == "<7A129E26-2C1F-4517-B6B5-39460ED50E12@example.com>"
    )


def test_flags(message):
    # flag = 8623489089
    flag = (
        (1 << 0)  # read
        + (1 << 6)  # draft
        + (1 << 25)  # is not junk
        + (1 << 33)  # (something undocumented Apple adds)
    )
    flags = message.plist["flags"]
    assert flags == {"read": True, "draft": True, "is_not_junk": True}
