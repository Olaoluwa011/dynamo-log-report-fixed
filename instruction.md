# Access Log Summary

Analyze the Apache-style access log at `/app/access.log` and create a JSON report at `/app/report.json`.

Success criteria:

1. `/app/report.json` is valid JSON and contains exactly these keys: `total_requests`, `unique_ips`, and `top_path`.
2. `total_requests` is an integer equal to the number of non-empty request lines in `/app/access.log`.
3. `unique_ips` is an integer equal to the number of distinct client IP addresses in the log.
4. `top_path` is the requested URL path that occurs most often. If multiple paths tie, use the path whose first occurrence appears earliest in the log.
5. Do not modify `/app/access.log`.
