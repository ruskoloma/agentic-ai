#!/usr/bin/env python3
"""Course environment check — Agentic AI Engineering, Week 1."""
import platform, shutil, subprocess, sys

PASS, FAIL, WARN = "[ OK ]", "[FAIL]", "[WARN]"
problems = 0

def check(label, ok, fix="", warn_only=False):
    global problems
    tag = PASS if ok else (WARN if warn_only else FAIL)
    print(f"{tag} {label}")
    if not ok:
        if not warn_only:
            problems += 1
        if fix:
            print(f"       fix: {fix}")

# 1. Python version
v = sys.version_info
check(f"Python {v.major}.{v.minor}.{v.micro} (need 3.10+)", (v.major, v.minor) >= (3, 10),
      "install a current Python from python.org")

# 2. pip available
try:
    import pip  # noqa
    pip_ok = True
except ImportError:
    pip_ok = subprocess.run([sys.executable, "-m", "pip", "--version"],
                            capture_output=True).returncode == 0
check("pip is available", pip_ok, "python -m ensurepip --upgrade")

# 3. venv module
venv_ok = subprocess.run([sys.executable, "-m", "venv", "--help"],
                         capture_output=True).returncode == 0
check("venv module works", venv_ok, "on Debian/Ubuntu: sudo apt install python3-venv")

# 4. requests importable (installed inside the course venv in Lab 0)
try:
    import requests  # noqa
    check("requests library installed", True)
except ImportError:
    check("requests library installed", False, "pip install requests  (inside your activated venv)")

# 5. git
check("git installed", shutil.which("git") is not None, "install from git-scm.com")

# 6. disk space for Week 4 model downloads
free_gb = shutil.disk_usage(".").free / 1e9
check(f"free disk: {free_gb:.0f} GB (want 8+ for models)", free_gb >= 8, warn_only=True)

# 7. OS report (informational)
print(f"[info] OS: {platform.system()} {platform.release()} · machine: {platform.machine()}")

print()
print("ALL CHECKS PASSED — your machine is ready for the course." if problems == 0
      else f"{problems} problem(s) above — fix and re-run. Stuck? Bring this output to class.")
sys.exit(problems)
