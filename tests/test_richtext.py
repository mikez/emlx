import os.path

import pytest

import emlx


TEST_FILE = "richtext.emlx"
TEST_HTML_LENGTH = 291
TEST_PAYLOAD_LENGTH = 291


# Fixtures


@pytest.fixture
def message_filepath(request):
    dirname = os.path.dirname(request.module.__file__)
    return f"{dirname}/{TEST_FILE}"


@pytest.fixture
def message(message_filepath):
    return emlx.read(message_filepath)


# Tests


def test_message_mime_content(message):
    assert message.text is None
    assert len(message.html) == TEST_HTML_LENGTH
    assert len(message.get_payload()) == TEST_PAYLOAD_LENGTH
