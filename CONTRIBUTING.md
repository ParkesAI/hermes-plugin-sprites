# Contributing

Open issues and pull requests against this repository for changes to the fork.
Include the Hermes revision, plugin revision, steps to reproduce, and expected
and actual behavior. Remove tokens, account identifiers and private logs before
posting. Never include a real `SPRITES_TOKEN` in an issue, fixture or test.

## Development and tests

Clone this plugin and [Hermes Agent](https://github.com/NousResearch/hermes-agent)
as sibling directories. CI pins Hermes to
`2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`; changes to that pin should be
reviewed alongside the resulting test run.

From the Hermes checkout, run:

```bash
scripts/run_tests.sh \
  ../hermes-plugin-sprites/tests/test_sprites_environment.py \
  ../hermes-plugin-sprites/tests/test_background_launch.py
```

The runner provisions the locked test environment. Unit tests require no cloud
credentials. Tests that inspect the real SDK may skip when it is unavailable;
the SDK-independent regression tests still run. The legacy live test file is
not part of CI; see the README before attempting live testing.

Keep fixes focused and include a regression test. Background-launch changes
must preserve PID reporting, output logs and the command's actual exit code,
including paths with spaces and shell metacharacters. Commands that do not
match Hermes' managed-launch contract must pass through unchanged.

## Upstream changes

Keep `upstream` pointed at `NousResearch/hermes-plugin-sprites`. Fetch and review
upstream changes before rebasing a contribution. Keep fork-specific fixes
separate from upstream commits so they can be proposed upstream or removed when
upstream incorporates an equivalent fix.

Contributions are provided under the [MIT license](LICENSE). Preserve existing
copyright notices and attribution.
