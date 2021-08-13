import pytest
from impo.span import Span, InvalidSpan

class TestSpanValidation:
    def test_valid(self, n):
        span = Span(1, n)
        assert span.validate(n)

    def test_invalid_n(self, n):
        span = Span(1, n+1)
        with pytest.raises(InvalidSpan):
            span.validate(n)

    def test_invalid_start(self, n):
        with pytest.raises(InvalidSpan):
            Span(0, n+1)

    def test_invalid_end(self, n):
        with pytest.raises(InvalidSpan):
            Span(n, n-10)
