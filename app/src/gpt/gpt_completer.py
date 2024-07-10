import aiohttp
import typing as tp
from app.src.gpt.content_type import ContentType
from app.src.internal import env
from app.src.gpt.message import Message, assistant_message


class GptCompleter:
    def __init__(self, system_prompt: str) -> None:
        self._system_prompt = system_prompt

    async def complete(self, input: list[Message]) -> Message:
        assert len(input) > 0
        messages: list[dict[str, tp.Any]] = []
        messages.append(
            {
                "role": "system",
                "content": [{"type": "text", "text": self._system_prompt}],
            }
        )
        for item in input:
            if item.content_type() == ContentType.Image:
                obj = [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{item.content()}"},
                    }
                ]
            elif item.content_type() == ContentType.Text:
                obj = [{"type": "text", "text": item.content()}]
            else:
                raise RuntimeError(f"Invalid content type: {item.content_type()}")
            messages.append({"role": item.role(), "content": obj})
        content = await self._complete(messages)
        return assistant_message(content)

    async def _complete(self, messages: list[dict[str, tp.Any]]) -> str:
        data = await _post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": "gpt-4o",
                "max_tokens": 4000,
                "temperature": 0,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "messages": messages,
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {env.OPENAI_API_KEY()}",
            },
        )
        return data["choices"][0]["message"]["content"]


async def _post(
    url: str, json: dict[str, tp.Any], headers: dict[str, str]
) -> dict[str, tp.Any]:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json, headers=headers) as response:
            response.raise_for_status()
            return await response.json()
