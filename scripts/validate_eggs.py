#!/usr/bin/env python3
"""Validate every egg-*.json in the repository.

    python3 scripts/validate_eggs.py               # offline checks
    python3 scripts/validate_eggs.py --check-urls  # also verify the URLs resolve

Checks: valid JSON + required PTDL_v2 keys, unique uuid, no carriage returns in
any string, required variables, safe EULA handling, `bash -n` on the installer
and on the embedded pelican-start.sh, icon present, and that the committed JSON
matches what scripts/generate_eggs.py produces.
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = ["name", "author", "uuid", "description", "image", "features", "docker_images",
                 "startup", "config", "scripts", "variables"]
REQUIRED_VARS = ["AUTO_UPDATE", "JVM_OPTS", "MOTD", "ALLOW_FLIGHT", "MAX_PLAYERS", "ONLINE_MODE",
                 "ENABLE_WHITELIST", "WHITELIST_USERS", "OP_USERS"]

errors = []


def err(file, msg):
    errors.append(f"{file}: {msg}")
    print(f"❌ {file}: {msg}")


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from strings(k)
            yield from strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v)


def bash_syntax(file, label, script):
    r = subprocess.run(["bash", "-n"], input=script, text=True, capture_output=True)
    if r.returncode != 0:
        err(file, f"bash -n failed for {label}: {r.stderr.strip()}")


def url_ok(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "validate-eggs"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    check_urls = "--check-urls" in sys.argv[1:]
    files = sorted(ROOT.glob("**/egg-*.json"))
    if not files:
        print("No egg-*.json files found")
        return 1
    uuids = {}
    for path in files:
        rel = path.relative_to(ROOT)
        raw = path.read_bytes()
        if b"\r" in raw:
            err(rel, "file contains a carriage return (CRLF)")
        try:
            egg = json.loads(raw)
        except json.JSONDecodeError as e:
            err(rel, f"invalid JSON: {e}")
            continue

        if egg.get("meta", {}).get("version") != "PTDL_v2":
            err(rel, "meta.version must be PTDL_v2")
        for k in REQUIRED_KEYS:
            if not egg.get(k):
                err(rel, f"missing or empty key: {k}")
        if any("\r" in s for s in strings(egg)):
            err(rel, "a string value contains \\r (would break shebang lines)")
        if egg.get("uuid") in uuids:
            err(rel, f"duplicate uuid also used by {uuids[egg['uuid']]}")
        uuids[egg.get("uuid")] = rel

        if "bash ./pelican-start.sh" not in egg.get("startup", ""):
            err(rel, "startup must run 'bash ./pelican-start.sh'")
        if "eula" not in egg.get("features", []):
            err(rel, "'eula' feature must be enabled")

        env = {v["env_variable"]: v for v in egg.get("variables", [])}
        for name in REQUIRED_VARS:
            if name not in env:
                err(rel, f"missing variable {name}")
        if "AUTO_UPDATE" in env and "boolean" in env["AUTO_UPDATE"]["rules"].split("|"):
            err(rel, "AUTO_UPDATE must not use the 'boolean' rule (rejects the string 'true')")

        icon = ROOT / Path(egg.get("image", "")).parent.name / "icon.png"
        if not icon.is_file() or icon.stat().st_size == 0:
            err(rel, f"icon missing or empty: {icon.relative_to(ROOT)}")

        script = egg.get("scripts", {}).get("installation", {}).get("script", "")
        bash_syntax(rel, "installation script", script)
        m = re.search(r"<< 'EOF' > pelican-start\.sh\n(.*?)\nEOF\n", script, re.S)
        if not m:
            err(rel, "could not find the pelican-start.sh heredoc in the installation script")
        else:
            start = m.group(1) + "\n"
            bash_syntax(rel, "pelican-start.sh", start)
            if "EULA=\"true\"" in start and "grep -qi '^eula=true'" not in start:
                err(rel, "pelican-start.sh exports EULA=true without checking eula.txt")
        if re.search(r"echo\s+\"?eula=true", script.split("<< 'EOF'")[0]):
            err(rel, "installer must not accept the EULA on the user's behalf")
        if "set -euo pipefail" not in script:
            err(rel, "installer must use 'set -euo pipefail' so failed downloads fail the install")
        if "curl -sSL" in script:
            err(rel, "use curl -fsSL (without -f an HTTP error page is saved as the file)")

        if check_urls:
            urls = [egg["meta"]["update_url"], egg["image"]]
            repo = re.search(r'REPO="([^"]+)"', script)
            if repo:
                urls += [f"https://raw.githubusercontent.com/{repo.group(1)}/main/{f}" for f in ("launch.sh", "pack.env")]
                urls.append(f"https://api.github.com/repos/{repo.group(1)}/releases/latest")
            for u in urls:
                if not url_ok(u):
                    err(rel, f"URL not reachable: {u}")
        print(f"✅ {rel}" if not any(str(rel) in e for e in errors) else f"⚠️  {rel} has problems")

    gen = subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_eggs.py"), "--check"],
                         capture_output=True, text=True)
    if gen.returncode != 0:
        err("generator", gen.stdout.strip() or gen.stderr.strip())

    print(f"\n{len(errors)} problem(s)" if errors else "\nAll eggs valid.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
