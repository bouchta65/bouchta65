from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
GENERATOR = ROOT / "ascii_to_svg.py"
COUNTER_URL = "https://komarev.com/ghpvc/?username=bouchta65&label=Profile%20views&color=0e75b6&style=flat"


def fetch_profile_views() -> str:
    url = f"{COUNTER_URL}&_={int(time.time())}"
    request = Request(
        url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": "bouchta65-profile-svg-updater",
        },
    )
    with urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8", errors="replace")

    text_values = re.findall(r">(.*?)<", svg)
    for value in reversed(text_values):
        cleaned = value.strip()
        if re.fullmatch(r"\d[\d,.\s]*", cleaned):
            return cleaned.replace(" ", "")

    raise RuntimeError("Could not find the Komarev profile views number.")


def update_generator_number(number: str) -> None:
    source = GENERATOR.read_text(encoding="utf-8")
    updated, count = re.subn(
        r'\("badge",\s*"Profile views",\s*"[^"]+"\)',
        f'("badge", "Profile views", "{number}")',
        source,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not update the profile views value in ascii_to_svg.py.")
    GENERATOR.write_text(updated, encoding="utf-8")


def main() -> None:
    number = fetch_profile_views()
    update_generator_number(number)
    subprocess.run([sys.executable, str(GENERATOR)], cwd=ROOT, check=True)
    print(f"Profile views updated to {number}.")


if __name__ == "__main__":
    main()
