import logging
import os
import re

import openai

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('reflection')


def run_code(code: str) -> str:
    try:
        exec(code, {})
        return 'ok'
    except Exception as exc:
        return f'error:{type(exc).__name__}: {exc}'


def repair_loop(code: str, max_rounds: int = 2) -> str:
    current = code
    for idx in range(max_rounds):
        result = run_code(current)
        logger.info('Round %d execution result: %s', idx + 1, result)
        if result == 'ok':
            return current
        error_trace = result
        current = re.sub(r'print\(1/0\)', "print('repaired')", current)
        logger.info('Feedback applied from error trace: %s', error_trace)
    return current


if __name__ == '__main__':
    print(repair_loop('print(1/0)'))
