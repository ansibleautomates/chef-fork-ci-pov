"""Confirm a test-only secret is usable without printing its value."""

import json
import os

value = os.environ.get("CHEF_POV_CANARY", "")
assert value and not value.startswith(("<+", "${{")), "canary secret was not resolved"
print(json.dumps({"canary_resolved": True, "purpose": "synthetic-pov-only"}))
