# tests/test_validator.py

import pytest
from content_validator import check_title_length
from content_validator import check_body_contains_keyword

@pytest.mark.parametrize("title,expected", [
    ("Short title",         True),   # clearly short
    ("X" * 60,              True),   # right at the limit
    ("X" * 61,              False),  # one char above
    ("Exact sixty chars 1234567890ABCDEFGHIJ", True),  # real example
])
def test_check_title_length(title, expected):
    """
    Tests different titles to validate that the
    check_title_length function returns the expected result.
    """
    assert check_title_length(title) is expected


@pytest.mark.parametrize("body, keyword, expected", [
    ("This text mentions Python and pytest.",        "pytest",   True),   # exact match
    ("Case INSENSITIVE check works for PyTest too.", "pytest",   True),   # case-insensitive
    ("Keyword as substring: testing",                "test",     True),   # substring match
    ("No match here at all.",                        "pytest",   False),  # absent
    ("Punctuation around pytest!",                   "pytest",   True),   # with punctuation
    ("partialpythongrammar",                         "python",   True),   # substring inside word
    ("",                                             "anything", False),  # empty body
])
def test_check_body_contains_keyword(body, keyword, expected):
    """
    Verifies that check_body_contains_keyword detects the presence (or absence)
    of the keyword, regardless of case or punctuation.
    """
    assert check_body_contains_keyword(body, keyword) is expected

# tests/test_validator.py


from types import SimpleNamespace
import content_validator as cv

@pytest.mark.parametrize("model_response,expected", [
    (" yes",   True),    # affirmative response
    ("Yes ",   True),    # uppercase and spaces
    ("no",     False),   # negative response
    ("Nope",   False),   # another negation
])
def test_is_fully_localized(monkeypatch, model_response, expected):
    """
    Simulates the LLM response from _client.chat.completions.create
    and checks that is_fully_localized() returns True only if it starts with 'yes'.
    """

    # Create a dummy response with the same structure as returned by OpenAI
    dummy_resp = SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content=model_response)
        )]
    )

    # Monkeypatching create() to return dummy_resp
    monkeypatch.setattr(
        cv._client.chat.completions,
        "create",
        lambda *args, **kwargs: dummy_resp
    )

    # Now the function will use our dummy_resp
    result = cv.is_fully_localized("some text", "nl_NL")
    assert result is expected
