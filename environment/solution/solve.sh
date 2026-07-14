#!/bin/bash
set -euo pipefail

python - <<'PY'
import json
from collections import Counter
from pathlib import Path

log_path = Path("/app/access.log")
report_path = Path("/app/report.json")

total_requests = 0
ip_addresses = set()
path_counts = Counter()
path_order = []

for raw_line in log_path.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()

    if not line:
        continue

    parts = line.split()
    ip_address = parts[0]
    request = line.split('"')[1]
    path = request.split()[1]

    total_requests += 1
    ip_addresses.add(ip_address)
    path_counts[path] += 1

    if path not in path_order:
        path_order.append(path)

top_path = max(path_order, key=lambda item: path_counts[item])

report = {
    "total_requests": total_requests,
    "unique_ips": len(ip_addresses),
    "top_path": top_path,
}

report_path.write_text(
    json.dumps(report, indent=2) + "\n",
    encoding="utf-8",
)
PY
