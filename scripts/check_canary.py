"""Confirm a test-only secret is usable without printing its value."""

import hashlib
import json
import os

value = os.environ.get("CHEF_POV_CANARY", "")
assert value and not value.startswith(("<+", "${{")), "canary secret was not resolved"
# This contributor-controlled probe touches only the explicitly supplied fake
# canary, never connector credentials or other environment variables.
print(json.dumps({
    "canary_resolved": True,
    "contributor_code_executed": True,
    "canary_readable_by_contributor_code": True,
    "canary_sha256": hashlib.sha256(value.encode()).hexdigest(),
    "purpose": "synthetic-pov-only",
}))
