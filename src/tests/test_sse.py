from promptools.utils.sse import Event


def test_event():
    assert Event("test") == Event("test"), "events have __hash__ and __eq__"
    assert str(Event("test")) != str(Event("test")), "the id field is different"
