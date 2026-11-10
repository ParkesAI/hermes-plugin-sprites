"""Real shell regression: a detached job must not hold the exec pipe open."""
import shlex
import subprocess
import time
from pathlib import Path

from sprites_environment import _detach_hermes_background_launch


def wrapper(root, command):
    q = shlex.quote
    stem = root / 'hermes_bg_proc_a1b2'
    return (f"mkdir -p {q(str(root))} && "
            f"( nohup bash -lc {q(command)} > {q(str(stem)+'.log')} 2>&1; "
            f"rc=$?; printf '%s\\n' \"$rc\" > {q(str(stem)+'.exit')} ) & "
            f"echo $! > {q(str(stem)+'.pid')} && cat {q(str(stem)+'.pid')}")


def test_launch_returns_before_job_and_preserves_log_and_failure(tmp_path):
    root = tmp_path / 'space and quote\'s'; root.mkdir()
    command = "sleep 1; printf 'job output\\n'; exit 7"
    transformed = _detach_hermes_background_launch(wrapper(root, command))
    launched = subprocess.run(['bash', '-c', transformed], capture_output=True,
                              text=True, timeout=0.7, check=True)
    assert launched.stdout.strip().isdigit()
    exit_path = root / 'hermes_bg_proc_a1b2.exit'
    deadline = time.monotonic() + 5
    while not exit_path.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    assert exit_path.read_text().strip() == '7'
    assert (root / 'hermes_bg_proc_a1b2.log').read_text() == 'job output\n'
    assert (root / 'hermes_bg_proc_a1b2.pid').read_text().strip() == launched.stdout.strip()


def test_non_launch_commands_and_mismatched_paths_are_unchanged(tmp_path):
    commands = ['readlink -f /tmp/file', 'cat /tmp/file', 'echo ordinary & wait',
                wrapper(tmp_path, 'true').replace('.exit', '.other')]
    for command in commands:
        assert _detach_hermes_background_launch(command) == command


def test_quoted_user_command_with_launch_like_text_is_preserved(tmp_path):
    command = "printf '%s' ' & echo $! > not-a-launch'"
    transformed = _detach_hermes_background_launch(wrapper(tmp_path, command))
    assert shlex.quote(command) in transformed
    assert transformed.endswith(' && cat ' + str(tmp_path / 'hermes_bg_proc_a1b2.pid'))
