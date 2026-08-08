import logging
import os

import openai

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('react')


def calculator(expr: str) -> str:
    try:
        return str(eval(expr, {'__builtins__': {}}, {}))
    except Exception as exc:
        return f'error:{exc}'


def react_loop(task: str, max_iterations: int = 3) -> str:
    thought = 'Need to solve the arithmetic task.'
    observation = ''
    for idx in range(max_iterations):
        logger.info('Iteration %d: thought=%s', idx + 1, thought)
        action = 'calculator' if 'calculate' in task.lower() or '+' in task else 'answer'
        if action == 'calculator':
            expr = task.replace('calculate', '').strip()
            observation = calculator(expr)
            thought = f'Observed result {observation}.'
            logger.info('Action=calculator expr=%s observation=%s', expr, observation)
        else:
            observation = 'No tool needed.'
            thought = 'Answer directly.'
            logger.info('Action=answer')
        if observation.startswith('error'):
            logger.warning('Tool failure, stopping early')
            return f'Failed: {observation}'
        if '=' in task:
            return observation
    logger.warning('Max iterations reached; triggering safeguard')
    return 'Stopped after max iterations'


if __name__ == '__main__':
    print(react_loop('calculate 7+8'))
