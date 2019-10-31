import logging

import pytest
from tenacity import stop_after_attempt

from retryer import retryer

retryer.logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize("cmd", [
    ["echo", "hello" ,"world"],
    ["echo2", "'test'"]
])
def test_retry_cmd_call_succeeds(cmd):
    retryer.execute.retry_with(stop=stop_after_attempt(0))(cmd)
    retryer.execute(cmd)
