from html import escape
import base64
from io import BytesIO
from pathlib import Path
import random
import re

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
INPUT_IMAGE = ROOT / "img" / "my image.png"
ASCII_TEXT = ROOT / "portrait.txt"
SVG_FILES = [ROOT / "dark.svg", ROOT / "light.svg"]
PROFILE_VIEWS_BADGE = "https://komarev.com/ghpvc/?username=bouchta65&amp;label=Profile%20views&amp;color=0e75b6&amp;style=flat"

COLS = 112
ROWS = 53
PORTRAIT_WIDTH = 96
START_X = 30
START_Y = 97.98
LINE_HEIGHT = 7.55

RAMP = " .:-=+*#%@"
PROFILE_REPLACEMENTS = {
    "sushmita@devos ~ % ./profile.sh --live": "bouchta65 ~ % ./profile.sh --live",
    "sushmita@devos": "bouchta65",
    "Subject": "Name",
    "Sushmita Dasari": "bouchta mohamed",
    "Origin": "Desc",
    "Andhra Pradesh, India": "The game changer",
    "B.Tech AI &amp; ML, CGPA 9.10": "BTS, LP, YOUCODE AI",
    "sushmitadasari17@gmail.com": "bouchtamohamed.ai@gmail.com",
    "videoportfolio-kohl.vercel.app": "soon",
    "sushmita-dasari-227a40284": "mohamed-bouchta-71082a286",
    "Sushmitadasari": "bouchta65",
}
INFO_ROWS = [
    ("head", "bouchta65", ""),
    ("field", "Name", "bouchta mohamed"),
    ("field", "Role", "AI/ML Developer"),
    ("field", "Desc", "The game changer"),
    ("field", "Education", "BTS, LP, YOUCODE AI"),
    ("field", "Status", "Building - Deploying - Securing"),
    ("field", "Tech.Stack", "Web Dev, Data, AI"),
    ("blank", "", ""),
    ("field", "AI.Code", "MLOps / LLMOps"),
    ("field", "Tools", "Docker, Kubernetes, Git, CI/CD"),
    ("cont", "", "MLflow, Prometheus, Grafana"),
    ("cont", "", "Arize Phoenix"),
    ("field", "BigData.BI", "Apache Spark, Apache Airflow"),
    ("cont", "", "Power BI, Snowflake"),
    ("field", "DB", "MySQL, PostgreSQL, MongoDB"),
    ("field", "Vector.DB", "ChromaDB, Weaviate, Neo4j"),
    ("blank", "", ""),
    ("section", "- Contact", ""),
    ("field", "Mail", "bouchtamohamed.ai@gmail.com"),
    ("field", "Portfolio", "soon"),
    ("field", "LinkedIn", "mohamed-bouchta-71082a286"),
    ("field", "Github", "bouchta65"),
    ("blank", "", ""),
    ("section", "- Profile Pulse", ""),
    ("badge", "Profile views", "4,743"),
]
PHOTO_X = 30
PHOTO_Y = 78
PHOTO_WIDTH = 458
PHOTO_HEIGHT = 426
PANEL_X = 14
PANEL_Y = 26
PANEL_WIDTH = 488
PANEL_HEIGHT = 468


def image_to_ascii(path: Path) -> list[str]:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        image = image.crop(bbox)

    image = ImageOps.contain(image, (PORTRAIT_WIDTH, ROWS), Image.Resampling.LANCZOS)
    image = image.resize((PORTRAIT_WIDTH, image.height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (COLS, ROWS), (0, 0, 0, 0))
    offset = ((COLS - image.width) // 2, ROWS - image.height)
    canvas.alpha_composite(image, offset)

    alpha = canvas.getchannel("A")
    gray = ImageOps.grayscale(canvas)
    gray = ImageEnhance.Contrast(gray).enhance(1.45)

    lines = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            opacity = alpha.getpixel((x, y))
            if opacity < 18:
                row.append(" ")
                continue

            luminance = gray.getpixel((x, y))
            shade = int((255 - luminance) / 255 * (len(RAMP) - 1))
            if opacity < 180:
                shade = max(1, shade - 2)
            row.append(RAMP[shade])
        lines.append("".join(row).rstrip())
    return lines


def lines_to_tspans(lines: list[str]) -> str:
    tspans = []
    for index, line in enumerate(lines):
        y = START_Y + (index * LINE_HEIGHT)
        tspans.append(
            f'<tspan x="{START_X}" y="{y:.2f}" xml:space="preserve">{escape(line)}</tspan>'
        )
    return "\n".join(tspans)


def image_data_uri(path: Path) -> str:
    image = Image.open(path).convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox:
        image = image.crop(bbox)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def build_fragment_rects(fill: str, css_class: str) -> str:
    rng = random.Random()
    rects = []
    cols = 28
    rows = 24
    cell_w = PANEL_WIDTH / cols
    cell_h = PANEL_HEIGHT / rows

    for row in range(rows):
        for col in range(cols):
            x = PANEL_X + (col * cell_w) - rng.uniform(1.0, 4.0)
            y = PANEL_Y + (row * cell_h) - rng.uniform(1.0, 4.0)
            width = cell_w + rng.uniform(2.0, 8.0)
            height = cell_h + rng.uniform(2.0, 8.0)
            delay = rng.uniform(0.0, 0.38)
            drift_x = rng.uniform(-46.0, 52.0)
            drift_y = rng.uniform(-38.0, 44.0)
            rotate = rng.uniform(-34.0, 34.0)
            start = 0.65 + delay
            rects.append(
                f'<rect class="{css_class}" x="{x:.2f}" y="{y:.2f}" '
                f'width="{width:.2f}" height="{height:.2f}" fill="{fill}" opacity="0" '
                f'style="--d:{delay:.3f}s; --tx:{drift_x:.2f}px; '
                f'--ty:{drift_y:.2f}px; --r:{rotate:.2f}deg">'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.9s" '
                f'begin="{start:.3f}s;visualReveal.mouseover+{delay:.3f}s" fill="freeze" '
                f'calcMode="spline" keySplines="0.16 1 0.3 1"/>'
                f'<animate attributeName="opacity" from="1" to="0" dur="0.72s" '
                f'begin="visualReveal.mouseout+{delay:.3f}s" fill="freeze" '
                f'calcMode="spline" keySplines="0.7 0 0.84 0"/>'
                f"</rect>"
            )

    return "\n    ".join(rects)


def build_reveal_defs() -> str:
    photo_rects = build_fragment_rects("#fff", "shard photo-shard")
    ascii_rects = build_fragment_rects("#000", "shard ascii-shard")
    seed_values = ";".join(str(random.randint(1, 999)) for _ in range(6))
    return f"""  <!-- Interactive portrait reveal: matching shard masks keep the real photo hidden until hover. -->
  <clipPath id="visualPanelClip">
    <rect x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}" rx="14"/>
  </clipPath>
  <mask id="photoShardMask" maskUnits="userSpaceOnUse" x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}">
    <rect x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}" fill="#000"/>
    {photo_rects}
  </mask>
  <mask id="asciiShardMask" maskUnits="userSpaceOnUse" x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}">
    <rect x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}" fill="#fff"/>
    {ascii_rects}
  </mask>
  <filter id="asciiFracture" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.018 0.22" numOctaves="2" seed="17" result="noise">
      <animate attributeName="seed" values="{seed_values}" dur="5.6s" repeatCount="indefinite"/>
      <animate attributeName="baseFrequency" values="0.018 0.22;0.052 0.18;0.026 0.32;0.018 0.22" dur="5.6s" repeatCount="indefinite"/>
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="0" xChannelSelector="R" yChannelSelector="G">
      <animate attributeName="scale" values="0;0;34;9;0;42;12;0" keyTimes="0;0.17;0.27;0.37;0.60;0.70;0.80;1" dur="5.6s" repeatCount="indefinite"/>
      <animate attributeName="xChannelSelector" values="R;G;B;R" dur="11.2s" repeatCount="indefinite"/>
      <animate attributeName="yChannelSelector" values="G;B;R;G" dur="8.4s" repeatCount="indefinite"/>
    </feDisplacementMap>
  </filter>"""


def ensure_reveal_defs(svg: str) -> str:
    svg = re.sub(
        r"\n  <!-- Interactive portrait reveal:.*?</filter>",
        "",
        svg,
        flags=re.DOTALL,
    )
    return svg.replace("  <style>", build_reveal_defs() + "\n  <style>", 1)


def ensure_reveal_styles(svg: str) -> str:
    css = """    #visualReveal { cursor: crosshair; }
    .real-photo {
      image-rendering: auto;
      filter: saturate(1.04) contrast(1.04);
    }
    .ascii-fracture {
      filter: url(#asciiFracture);
      transform-origin: 258px 274px;
      animation: asciiMicroShift 5.6s cubic-bezier(0.18, 0.82, 0.2, 1) infinite;
    }
    #visualReveal:hover .ascii-fracture,
    #visualReveal:focus .ascii-fracture {
      transform: translate(10px, -5px) skewX(-2deg);
    }
    @keyframes asciiMicroShift {
      0%, 17%, 39%, 60%, 84%, 100% { transform: translate(0, 0) skewX(0deg) scale(1); }
      23% { transform: translate(-16px, 7px) skewX(4deg) scale(1.02); }
      29% { transform: translate(19px, -10px) skewX(-5deg) scale(0.99); }
      70% { transform: translate(22px, -11px) skewX(-5deg) scale(0.99); }
      76% { transform: translate(-14px, 8px) skewX(4deg) scale(1.02); }
    }
    .shard {
      opacity: 0;
      transform-box: fill-box;
      transform-origin: center;
      transform: translate(0, 0) rotate(0deg) scale(0.04);
      transition: opacity 0.12s linear var(--d), transform 1.05s cubic-bezier(0.18, 0.82, 0.2, 1) var(--d);
    }
    #visualReveal:hover .shard,
    #visualReveal:focus .shard {
      opacity: 1;
      transform: translate(var(--tx), var(--ty)) rotate(var(--r)) scale(1.55);
    }
"""
    svg = re.sub(
        r"    #visualReveal \{.*?(?=    \.cursor-blink)",
        "",
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(
        r"\.key    \{ font-family: 'Courier New', Consolas, monospace; font-size: \d+px;",
        ".key    { font-family: 'Courier New', Consolas, monospace; font-size: 16px;",
        svg,
    )
    svg = re.sub(
        r"\.value  \{ font-family: 'Courier New', Consolas, monospace; font-size: \d+px;",
        ".value  { font-family: 'Courier New', Consolas, monospace; font-size: 16px;",
        svg,
    )
    svg = re.sub(
        r"\.cc     \{ font-family: 'Courier New', Consolas, monospace; font-size: \d+px;",
        ".cc     { font-family: 'Courier New', Consolas, monospace; font-size: 16px;",
        svg,
    )
    return svg.replace("    .cursor-blink", css + "    .cursor-blink", 1)


def ensure_xlink_namespace(svg: str) -> str:
    if "xmlns:xlink" in svg:
        return svg
    return svg.replace(
        '<svg xmlns="http://www.w3.org/2000/svg"',
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"',
        1,
    )


def ensure_photo_layer(svg: str, data_uri: str) -> str:
    svg = re.sub(
        r'\n  <!-- Sharp source image sits underneath;.*?<!-- /portrait reveal -->\n',
        "",
        svg,
        flags=re.DOTALL,
    )
    visual = f"""
  <!-- Sharp source image sits underneath; shard masks reveal it while cutting away the vector ASCII. -->
  <g id="visualReveal" tabindex="0" clip-path="url(#visualPanelClip)">
    <image class="real-photo" x="{PHOTO_X}" y="{PHOTO_Y}" width="{PHOTO_WIDTH}" height="{PHOTO_HEIGHT}" preserveAspectRatio="xMidYMax meet" href="{data_uri}" xlink:href="{data_uri}" opacity="0">
      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.22;0.34;0.62;0.78;1" dur="5.6s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.16 1 0.3 1;0.4 0 0.2 1;0.7 0 0.84 0;0.4 0 0.2 1"/>
    </image>
    <g class="ascii-fracture" mask="url(#asciiShardMask)">
      <animate attributeName="opacity" values="1;1;0.2;0.12;1;1" keyTimes="0;0.18;0.34;0.62;0.82;1" dur="5.6s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.2 1;0.16 1 0.3 1;0.4 0 0.2 1;0.7 0 0.84 0;0.4 0 0.2 1"/>
      <text x="30" y="0" class="ascii">
      </text>
    </g>
    <rect x="{PANEL_X}" y="{PANEL_Y}" width="{PANEL_WIDTH}" height="{PANEL_HEIGHT}" fill="#fff" opacity="0" pointer-events="all"/>
  </g>
  <!-- /portrait reveal -->
"""
    svg = re.sub(
        r'\n  <g mask="url\(#revealMask\)">\s*<text x="30" y="0" class="ascii">.*?</text>\s*</g>\s*',
        "",
        svg,
        count=1,
        flags=re.DOTALL,
    )
    if '<g id="visualReveal"' not in svg:
        svg = svg.replace(
            '  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>\n',
            '  <text x="30" y="24" class="panel-title">VISUAL.MAP</text>\n' + visual,
            1,
        )
    return svg


def replace_ascii_block(svg: str, tspans: str) -> str:
    pattern = re.compile(
        r'(<text x="30" y="0" class="ascii">\s*)'
        r".*?"
        r'(\s*</text>)',
        re.DOTALL,
    )
    return pattern.sub(r"\1\n" + tspans + r"\2", svg, count=1)


def replace_profile_data(svg: str) -> str:
    for old, new in PROFILE_REPLACEMENTS.items():
        svg = svg.replace(old, new)
    svg = svg.replace('cx="1122"', 'cx="1088"')
    svg = svg.replace('x="1132" y="24" class="scan-label"', 'x="1098" y="24" class="scan-label"')
    return svg


def build_system_info(fill: str) -> str:
    groups = []
    line_start_x = 520
    dots_x = 625
    value_x = 870
    dots_width = value_x - dots_x - 14
    line_y = 42
    line_height = 16

    for index, (kind, label, value) in enumerate(INFO_ROWS):
        y = line_y + (index * line_height)
        if kind == "head":
            content = (
                f'<tspan x="{line_start_x}" y="{y}" class="head">{escape(label)}</tspan>'
                '<tspan class="cc"> ------------------------------------------------</tspan>'
            )
        elif kind == "section":
            content = (
                f'<tspan x="{line_start_x}" y="{y}" class="accent">{escape(label)}</tspan>'
                '<tspan class="cc"> ------------------------------------------------</tspan>'
            )
        elif kind == "field":
            label_text = f"{label}:"
            dots = "." * 46
            content = (
                f'<tspan x="{line_start_x}" y="{y}" class="key">{escape(label_text)}</tspan>'
                f'<tspan x="{dots_x}" y="{y}" class="cc" textLength="{dots_width}" lengthAdjust="spacing">{dots}</tspan>'
                f'<tspan x="{value_x}" y="{y}" class="value">{escape(value)}</tspan>'
            )
        elif kind == "cont":
            dots = "." * 46
            content = (
                f'<tspan x="{line_start_x}" y="{y}" class="key">...</tspan>'
                f'<tspan x="{dots_x}" y="{y}" class="cc" textLength="{dots_width}" lengthAdjust="spacing">{dots}</tspan>'
                f'<tspan x="{value_x}" y="{y}" class="value">{escape(value)}</tspan>'
            )
        elif kind == "note":
            content = (
                f'<tspan x="{line_start_x}" y="{y}" class="cc">. </tspan>'
                f'<tspan class="value">{escape(value)}</tspan>'
            )
        elif kind == "badge":
            badge_x = 608
            badge_y = y + 12
            number_center_x = badge_x + 173 + 140
            komarev_scale = 1.8
            komarev_width = 151 * komarev_scale
            komarev_height = 20 * komarev_scale
            komarev_number_start = 98 * komarev_scale
            komarev_number_width = 53 * komarev_scale
            komarev_x = number_center_x - ((98 + 26.5) * komarev_scale)
            komarev_y = badge_y + 1
            clip_x = komarev_x + komarev_number_start
            content = (
                f'<rect x="{badge_x}" y="{badge_y}" width="455" height="38" rx="5" fill="#020617" opacity="0.74" stroke="url(#borderGrad)" stroke-width="1"/>'
                f'<rect x="{badge_x + 1}" y="{badge_y + 1}" width="172" height="36" rx="4" fill="#0E75B6" opacity="0.88"/>'
                f'<rect x="{badge_x + 173}" y="{badge_y + 1}" width="281" height="36" rx="4" fill="#0F172A" opacity="0.76"/>'
                f'<text x="{badge_x + 86}" y="{badge_y + 24}" fill="#FFFFFF" text-anchor="middle" class="value">{escape(label)}</text>'
                f'<text x="{number_center_x}" y="{badge_y + 25}" fill="#FFFFFF" text-anchor="middle" font-size="18" font-weight="800" letter-spacing="1.2">{escape(value)}</text>'
                f'<clipPath id="profileViewsNumberClip"><rect x="{clip_x:.1f}" y="{komarev_y:.1f}" width="{komarev_number_width:.1f}" height="{komarev_height:.1f}" rx="4"/></clipPath>'
                f'<image x="{komarev_x:.1f}" y="{komarev_y:.1f}" width="{komarev_width:.1f}" height="{komarev_height:.1f}" preserveAspectRatio="none" href="{PROFILE_VIEWS_BADGE}" xlink:href="{PROFILE_VIEWS_BADGE}" clip-path="url(#profileViewsNumberClip)"/>'
            )
        else:
            content = f'<tspan x="{line_start_x}" y="{y}" class="cc">. </tspan>'

        if kind == "badge":
            groups.append(f"<g>{content}</g>")
        else:
            groups.append(f'<g><text x="520" y="0" fill="{fill}">{content}</text></g>')

    return "".join(groups)


def replace_system_info(svg: str) -> str:
    pattern = re.compile(
        r'(?<=<text x="524" y="24" class="panel-title">SYSTEM\.INFO</text>\n\n)'
        r".*?"
        r'(?=\n\n  <rect x="522")',
        re.DOTALL,
    )
    match = pattern.search(svg)
    if not match:
        return svg
    fill_match = re.search(r'fill="(#[0-9A-Fa-f]{6})"', match.group(0))
    fill = fill_match.group(1) if fill_match else "#dbeafe"
    return svg[: match.start()] + "  " + build_system_info(fill) + svg[match.end() :]


def main() -> None:
    lines = image_to_ascii(INPUT_IMAGE)
    ASCII_TEXT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    tspans = lines_to_tspans(lines)
    data_uri = image_data_uri(INPUT_IMAGE)
    for svg_file in SVG_FILES:
        svg = svg_file.read_text(encoding="utf-8")
        svg = ensure_xlink_namespace(svg)
        svg = ensure_reveal_defs(svg)
        svg = ensure_reveal_styles(svg)
        svg = ensure_photo_layer(svg, data_uri)
        svg = replace_profile_data(svg)
        svg = replace_system_info(svg)
        svg_file.write_text(replace_ascii_block(svg, tspans), encoding="utf-8")

    print(f"Generated {len(lines)} ASCII rows and updated {len(SVG_FILES)} SVG files.")


if __name__ == "__main__":
    main()
