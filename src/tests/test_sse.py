from promptools.stream.sse import Event, as_event_stream


def test_event():
    assert Event("test") == Event("test"), "events have __hash__ and __eq__"
    assert str(Event("test")) != str(Event("test")), "the id field is different"


def test_stream_iterator():
    def stream():
        yield "data", "name", "id"

    assert list(as_event_stream(stream())) == [Event("data", "name", "id")]


def test_stream_iterator_function():
    @as_event_stream
    def stream():
        yield "data", "name", "id"

    assert list(stream()) == [Event("data", "name", "id")]


async def test_stream_async_iterator():
    async def stream():
        yield "data", "name", "id"

    assert [i async for i in as_event_stream(stream())] == [Event("data", "name", "id")]


async def test_stream_async_iterator_function():
    @as_event_stream
    async def stream():
        yield "data", "name", "id"

    assert [i async for i in stream()] == [Event("data", "name", "id")]
