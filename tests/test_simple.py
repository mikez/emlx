import io
import os.path

import pytest

import emlx


TEST_FILE = "test.emlx"
TEST_BYTECOUNT = 545
TEST_MESSAGE_ID = "<7A129E26-2C1F-4517-B6B5-39460ED50E12@example.com>"
TEST_PAYLOAD_LENGTH = 73
# raw_flags = 8623489089
# = (
#     (1 << 0)  # read
#     + (1 << 6)  # draft
#     + (1 << 25)  # is not junk
#     + (1 << 33)  # (something undocumented Apple adds)
# )
TEST_PLIST = {
    "conversation-id": 123456,
    "date-last-viewed": 1581111111,
    "date-received": 1581000000,
    "flags": {"read": True, "draft": True, "is_not_junk": True},
    "remote-id": "789",
}


@pytest.fixture
def message_filepath(request):
    dirname = os.path.dirname(request.module.__file__)
    return f"{dirname}/{TEST_FILE}"


@pytest.fixture
def message_content(message_filepath):
    with open(message_filepath, "rb") as filebuffer:
        return filebuffer.read()


@pytest.fixture
def message(message_filepath):
    return emlx.read(message_filepath)


def test_bytecount(message):
    assert message.bytecount == TEST_BYTECOUNT


def test_message_mime_content(message):
    assert message.headers["Message-Id"] == TEST_MESSAGE_ID
    assert message.id == TEST_MESSAGE_ID
    assert message.url == "message:" + TEST_MESSAGE_ID
    assert len(message.get_payload()) == TEST_PAYLOAD_LENGTH


def test_plist_and_flags(message):
    assert message.plist == TEST_PLIST
    assert message.flags == TEST_PLIST["flags"]


def test_message_buffered_as_bytesio(message_content):
    filebuffer = io.BytesIO(message_content)
    message = emlx.read(filebuffer)
    assert message.bytecount == TEST_BYTECOUNT
    assert message.id == TEST_MESSAGE_ID
    assert len(message.get_payload()) == TEST_PAYLOAD_LENGTH
    assert message.plist["flags"] == TEST_PLIST["flags"]


def test_message_buffered_via_open(message_filepath):
    with open(message_filepath, "rb") as filebuffer:
        message = emlx.read(filebuffer)
    assert message.bytecount == TEST_BYTECOUNT
    assert message.id == TEST_MESSAGE_ID
    assert len(message.get_payload()) == TEST_PAYLOAD_LENGTH
    assert message.plist["flags"] == TEST_PLIST["flags"]


def test_message_plist_only(message_filepath):
    message = emlx.read(message_filepath, plist_only=True)
    assert message.bytecount == TEST_BYTECOUNT
    assert message.url is None
    assert message.get_payload() is None
    assert message.plist == TEST_PLIST
    assert message.flags == TEST_PLIST["flags"]


def test_message_plist_only_as_bytesio(message_content):
    filebuffer = io.BytesIO(message_content)
    message = emlx.read(filebuffer, plist_only=True)
    assert message.bytecount == TEST_BYTECOUNT
    assert message.url is None
    assert message.get_payload() is None
    assert message.plist == TEST_PLIST
    assert message.flags == TEST_PLIST["flags"]


def test_message_plist_only_via_open(message_filepath):
    with open(message_filepath, "rb") as filebuffer:
        message = emlx.read(filebuffer, plist_only=True)
    assert message.bytecount == TEST_BYTECOUNT
    assert message.url is None
    assert message.get_payload() is None
    assert message.plist == TEST_PLIST
    assert message.flags == TEST_PLIST["flags"]
