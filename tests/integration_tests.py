import pytest

import siggler

model = "gpt-4o-mini"


def test_tool_call(client):
    @siggler.tool
    def get_weather(city: str, date: str) -> str:
        """
        Get the weather for a city on a specific date.
        Args:
            city: The city to get the weather for.
            date: The date to get the weather for.
        Returns: The weather in the city on the specified date.
        """
        return f"The weather in {city} was sunny on {date}."

    input_message = "What was the weather like in Edinburgh on 01-01-2000?"
    response = client.responses.parse(
        input=input_message, tools=[get_weather.signature], model=model
    )
    output = response.output[0]

    assert output.type == "function_call"
    weather_forecast = siggler.call(output.name, output.arguments)
    assert weather_forecast == "The weather in Edinburgh was sunny on 2000-01-01."

@pytest.mark.asyncio
async def test_tool_acall(client):

    @siggler.tool
    async def get_weather(city: str, date: str) -> str:
        """
        Get the weather for a city on a specific date.
        Args:
            city: The city to get the weather for.
            date: The date to get the weather for.
        Returns: The weather in the city on the specified date.
        """
        return f"The weather in {city} was sunny on {date}."

    input_message = "What was the weather like in Edinburgh on 01-01-2000?"
    response = client.responses.parse(
        input=input_message, tools=[get_weather.signature], model=model
    )
    output = response.output[0]

    assert output.type == "function_call"
    weather_forecast = await siggler.acall(output.name, output.arguments)
    assert weather_forecast == "The weather in Edinburgh was sunny on 2000-01-01."