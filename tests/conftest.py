import pytest
from openai import OpenAI, AsyncOpenAI


@pytest.fixture
def client() -> OpenAI:
    return OpenAI()


@pytest.fixture
def async_client() -> AsyncOpenAI:
    return AsyncOpenAI()
