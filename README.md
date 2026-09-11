# Fork PR CI proof of value

A small Python application that demonstrates a Git-backed Harness Unified pipeline and a pull request from a separate GitHub account. This repository contains no Chef source code. The application secret is a synthetic canary with no access to any service.

## Repositories and pipeline

- Upstream: [ansibleautomates/chef-fork-ci-pov](https://github.com/ansibleautomates/chef-fork-ci-pov).
- Contributor fork: [Ompragash/chef-fork-ci-pov](https://github.com/Ompragash/chef-fork-ci-pov).
- Test PR: [upstream PR #1](https://github.com/ansibleautomates/chef-fork-ci-pov/pull/1).
- Canonical pipeline: [`.harness/pipeline.yaml`](.harness/pipeline.yaml).

The YAML has no pipeline-level name or identifier. Harness keeps those in its pipeline registration. Stage and step IDs, a Git branch name, and references to the configured connector and secret remain in the YAML.

## What runs

1. Clone the requested branch or pull request.
2. Install test dependencies, compile the application, and prepare `dist/app.py`.
3. Run the example application.
4. Resolve the synthetic `chef_pov_canary` secret and pass it to `scripts/check_canary.py`.
5. Run pytest and generate JUnit, LCOV, coverage XML, and coverage HTML files.
6. Upload JUnit and LCOV to Harness Tests and Coverage. XML and HTML are generated locally in the runner, not separately published as downloadable artifacts.

The pipeline uses Harness Cloud, disables pipeline caching and persisted clone credentials, and has a 10-minute timeout. The upstream PR trigger reads the pipeline definition from upstream `main` while checking out PR code. It listens for PR open, synchronize, and reopen events targeting `main`.

## Observed results

The initial upstream run passed 8 tests with 88.9% line coverage. The contributor PR run passed 9 tests with 100% line coverage and posted a successful GitHub commit status.

The PR intentionally adds an `UNTRUSTED_PR_YAML_MARKER` command to its pipeline YAML. That command did not run because the trigger selected upstream `main` for the pipeline definition. The PR also changes `scripts/check_canary.py`, which did run from the PR checkout and successfully computed a SHA-256 digest of the supplied canary. The raw canary was not printed.

This demonstrates that an upstream-controlled pipeline can still expose a secret to contributor-controlled scripts. This is a reproduction of that behavior, not a secure design for running arbitrary contributor code with real secrets.

## Run locally

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-test.txt
.venv/bin/python app.py
.venv/bin/python -m pytest --junitxml=reports/junit.xml --cov=app --cov-report=lcov:reports/lcov.info
```

To register the pipeline elsewhere, configure the `chef_pov_github` connector and the synthetic `chef_pov_canary` secret in that Harness project. The missing pipeline name and identifier do not eliminate those environment dependencies. Running the fork in a separate contributor-owned Harness account has not been tested.
