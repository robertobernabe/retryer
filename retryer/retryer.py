import argparse
import os
import subprocess
import sys
from tenacity import retry, wait_random_exponential, stop_after_attempt, after_log

import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


@retry(
    wait=wait_random_exponential(multiplier=1, max=30),
    after=after_log(logger, logging.INFO),
)
def execute(cmd: list):
    logger.debug(f"execute: {cmd}")
    cp: subprocess.CompletedProcess = subprocess.run(
        cmd, shell=True, check=True, stdout=subprocess.PIPE)
    if cp.stdout:
        sys.stdout.write(str(cp.stdout, 'utf-8'))
    if cp.stderr:
        sys.stderr.write(str(cp.stderr, 'utf-8'))

    logger.debug(f"exitcode was: {cp.returncode}")
    if cp.returncode != 0:
        raise Exception(f"execution of [{cp.args}] failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retryer")
    parser.add_argument("cmd", type=str, nargs="+")
    parser.add_argument(
        "--retries", type=int, help="retries", default=3,
    )

    args = parser.parse_args()
    sys.exit(execute.retry_with(stop=stop_after_attempt(args.retries))(args.cmd))
