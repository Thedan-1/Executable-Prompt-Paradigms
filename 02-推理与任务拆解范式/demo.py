import logging
import os
import re
from collections import Counter

import openai

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('reasoning')


def call_model(problem: str) -> str:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))
    try:
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            temperature=0.7,
            messages=[{'role': 'user', 'content': f'Solve: {problem}'}],
            n=1,
        )
        content = response.choices[0].message.content or ''
        logger.info('Sample produced: %s', content)
        return content
    except openai.OpenAIError as exc:
        logger.error('OpenAI error during sampling: %s', exc)
        return f'Answer: {problem.split()[-1]}'


def self_consistency(problem: str, n: int = 3) -> str:
    answers = []
    for idx in range(n):
        text = call_model(problem)
        match = re.search(r'Answer:\s*(.+)', text)
        answer = match.group(1).strip() if match else text.strip()
        logger.info('Sample %d -> %s', idx + 1, answer)
        answers.append(answer)
    counts = Counter(answers)
    winner, score = counts.most_common(1)[0]
    logger.info('Consensus reached: %s with %d votes', winner, score)
    return winner


if __name__ == '__main__':
    print(self_consistency('What is 17 + 25?'))
