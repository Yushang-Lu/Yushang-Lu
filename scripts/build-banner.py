import argparse
from collections import defaultdict, deque
from pathlib import Path

from PIL import Image


def remove_background(source):
    image = Image.open(source).convert("RGB")
    width, height = image.size
    pixels = image.load()
    background = set()
    queue = deque(
        [(column, row) for column in range(width) for row in (0, height - 1)]
        + [(column, row) for row in range(height) for column in (0, width - 1)]
    )
    while queue:
        column, row = queue.popleft()
        if not (0 <= column < width and 0 <= row < height):
            continue
        if (column, row) in background or min(pixels[column, row]) < 230:
            continue
        background.add((column, row))
        queue.extend(
            [(column - 1, row), (column + 1, row), (column, row - 1), (column, row + 1)]
        )
    foreground = {
        (column, row)
        for row in range(height)
        for column in range(width)
        if (column, row) not in background
    }
    largest = set()
    while foreground:
        component = {foreground.pop()}
        queue = deque(component)
        while queue:
            column, row = queue.popleft()
            for neighbor in (
                (column - 1, row), (column + 1, row),
                (column, row - 1), (column, row + 1),
            ):
                if neighbor in foreground:
                    foreground.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        if len(component) > len(largest):
            largest = component
    cutout = image.convert("RGBA")
    cutout.putalpha(
        Image.frombytes(
            "L", image.size,
            bytes(255 if (column, row) in largest else 0
                  for row in range(height) for column in range(width)),
        )
    )
    return cutout.crop(cutout.getbbox())


def vectorize(image):
    thumbnail = image.resize((160, 144), Image.Resampling.BOX)
    palette_image = thumbnail.convert("RGB").quantize(colors=48)
    palette = palette_image.getpalette()
    colors = defaultdict(list)
    for row in range(thumbnail.height):
        column = 0
        while column < thumbnail.width:
            if thumbnail.getpixel((column, row))[3] < 128:
                column += 1
                continue
            color = palette_image.getpixel((column, row))
            end = column + 1
            while (
                end < thumbnail.width
                and thumbnail.getpixel((end, row))[3] >= 128
                and palette_image.getpixel((end, row)) == color
            ):
                end += 1
            colors[color].append(f"M{column} {row}h{end-column}v1h-{end-column}z")
            column = end
    return "\n".join(
        f'<path fill="#{"".join(f"{channel:02x}" for channel in palette[color*3:color*3+3])}" d="{"".join(paths)}"/>'
        for color, paths in colors.items()
    )


def build_banner(avatar):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="380" viewBox="0 0 1000 380" role="img" aria-labelledby="title description">
  <title id="title">Yushang Lu | Learning systems, building understanding</title>
  <desc id="description">HITSZ undergraduate in Shenzhen, China. Currently learning AI infrastructure. C, C++, and Python. A mint pixel-art avatar on a rounded midnight-blue banner.</desc>
  <defs>
    <linearGradient id="background" x2="1" y2="1">
      <stop stop-color="#101F2C"/><stop offset="1" stop-color="#172F3A"/>
    </linearGradient>
    <radialGradient id="glow">
      <stop stop-color="#6BDFC0" stop-opacity=".15"/><stop offset="1" stop-color="#6BDFC0" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="#9EE3D5" stroke-opacity=".045"/>
    </pattern>
    <clipPath id="rounded"><rect width="1000" height="380" rx="28"/></clipPath>
  </defs>
  <g clip-path="url(#rounded)">
    <rect width="1000" height="380" fill="url(#background)"/>
    <rect x="625" width="375" height="380" fill="url(#grid)"/>
    <ellipse cx="800" cy="182" rx="230" ry="220" fill="url(#glow)"/>
    <path d="M652 0V380" stroke="#A6DCCE" stroke-opacity=".10"/>
    <path d="M42 29H85" stroke="#87E5C8" stroke-width="3" stroke-linecap="round"/>
    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
      <text x="48" y="69" fill="#94ADBA" font-size="13" letter-spacing="2.6">A LITTLE CODE. A LOT OF CURIOSITY.</text>
      <text x="45" y="133" fill="#F0F6F5" font-size="57" font-weight="700" letter-spacing="-2">Yushang Lu<tspan fill="#87E5C8">.</tspan></text>
      <text x="48" y="166" fill="#A5BECA" font-size="16">@Yushang-Lu  /  HITSZ undergraduate</text>
      <text x="48" y="214" fill="#E0ECEA" font-size="23" font-weight="500">Learning systems.</text>
      <text x="48" y="244" fill="#E0ECEA" font-size="23" font-weight="500">Building understanding.</text>
      <rect x="48" y="271" width="212" height="32" rx="16" fill="#24443F" stroke="#87E5C8" stroke-opacity=".22"/>
      <circle cx="65" cy="287" r="3.5" fill="#87E5C8"/>
      <text x="77" y="292" fill="#A6EAD4" font-size="13" font-weight="600">CURRENT FOCUS · AI INFRA</text>
      <text x="280" y="292" fill="#C0CCD2" font-size="14">C / C++ / Python</text>
      <path d="M48 324H604" stroke="#A6DCCE" stroke-opacity=".15"/>
      <text x="48" y="350" fill="#95ADBA" font-size="12">SHENZHEN, CHINA</text>
      <text x="604" y="350" text-anchor="end" fill="#95ADBA" font-size="12">LEARN · EXPERIMENT · BUILD</text>
      <rect x="686" y="45" width="276" height="266" rx="22" fill="#10232C" fill-opacity=".50" stroke="#87E5C8" stroke-opacity=".18"/>
      <text x="705" y="72" fill="#90ADA9" font-size="10" letter-spacing="1.7">HELLO, WORLD</text>
      <circle cx="936" cy="68" r="3" fill="#87E5C8"/>
      <path d="M706 105V92H719M929 92H942V105M706 264V277H719M929 277H942V264" fill="none" stroke="#87E5C8" stroke-opacity=".45"/>
      <ellipse cx="824" cy="281" rx="84" ry="9" fill="#071A23" fill-opacity=".5"/>
      <g transform="translate(710 85) scale(1.42)" shape-rendering="crispEdges">{avatar}</g>
      <text x="824" y="346" text-anchor="middle" fill="#9BB5BB" font-family="'SFMono-Regular', Consolas, monospace" font-size="12">one small commit at a time.</text>
    </g>
  </g>
</svg>
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    arguments = parser.parse_args()
    assets = Path(__file__).resolve().parents[1] / "assets"
    cutout = remove_background(arguments.image)
    cutout.save(assets / "avatar-transparent.png")
    avatar = vectorize(cutout)
    (assets / "profile-banner.svg").write_text(build_banner(avatar))
    print("Created assets/avatar-transparent.png and assets/profile-banner.svg")


if __name__ == "__main__":
    main()
