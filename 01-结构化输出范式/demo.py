import json
import logging
import os
import re

import openai
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('structuring')


class StructuredResult(BaseModel):
    title: str = Field(default='fallback')
    summary: str = Field(default='fallback summary')
    priority: str = Field(default='low')


def sanitize_text(text: str) -> str:
    if not text:
        return ''
    text = re.sub(r'```(?:json|xml)?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*[{\[]', '{', text)
    text = re.sub(r'[}\]]\s*$', '}', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()


def parse_with_fallback(raw: str) -> StructuredResult:
    cleaned = sanitize_text(raw)
    try:
        payload = json.loads(cleaned)
        return StructuredResult.model_validate(payload)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        logger.warning('JSON parse failed: %s', exc)
        return StructuredResult(title='fallback', summary='schema fallback', priority='low')


def run_structured_demo(task: str) -> StructuredResult:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            temperature=0,
            messages=[
                {'role': 'system', 'content': 'Return compact JSON only.'},
                {'role': 'user', 'content': f'Task: {task}\nReturn JSON with title, summary, priority.'},
            ],
            response_format={'type': 'json_object'},
        )
        content = response.choices[0].message.content or '{}'
        logger.info('Model output received: %s', content)
        return parse_with_fallback(content)
    except openai.OpenAIError as exc:
        logger.error('OpenAI error: %s', exc)
        return StructuredResult(title='fallback', summary='api fallback', priority='low')


if __name__ == '__main__':
    result = run_structured_demo('Summarize a launch plan')
    logger.info('Final result: %s', result.model_dump())
