import os.path

import pytest

import emlx


TEST_FILE = "test.emlx"
# flags = 8623489089
# flags = (
#     (1 << 0)  # read
#     + (1 << 6)  # draft
#     + (1 << 25)  # is not junk
#     + (1 << 33)  # (something undocumented Apple adds)
# )
TEST_FLAGS = {"read": True, "draft": True, "is_not_junk": True}


@pytest.fixture
def message_filepath(request):
    dirname = os.path.dirname(request.module.__file__)
    return f"{dirname}/{TEST_FILE}"


@pytest.fixture
def message(message_filepath, request):
    return emlx.read(message_filepath)


def test_bytecount(message):
    assert message.bytecount == 545


def test_data(message):
    assert (
        message.data["Message-Id"]
        == "<7A129E26-2C1F-4517-B6B5-39460ED50E12@example.com>"
    )


def test_flags(message):
    assert message.plist["flags"] == TEST_FLAGS


def test_message_plist_only(message_filepath, request):
    message = emlx.read(message_filepath, plist_only=True)
    assert message.bytecount == 545
    assert message.data is None
    assert message.plist["flags"] == TEST_FLAGS
