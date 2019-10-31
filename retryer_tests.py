import pytest
from tenacity import stop_after_attempt

from retryer import retryer


@pytest.mark.parametrize("cmd", [
    ["echo", "hello" ,"world"],
    ["echo", "'test'"]
])
def test_retry_cmd_call_succeeds(cmd):
    retryer.execute.retry_with(stop=stop_after_attempt(0))(cmd)
    retryer.execute(cmd)
