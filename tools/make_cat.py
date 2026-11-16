"""Draw the original waving cat animation for the GitHub profile."""

from __future__ import annotations

import math
import pathlib
import shutil
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[1]
FRAMES = ROOT / "tools" / "cat-frames"
OUTPUT = ROOT / "assets" / "waving-cat.gif"
WIDTH, HEIGHT = 320, 220


def rgb(code: str) -> tuple[int, int, int]:
    return tuple(bytes.fromhex(code.lstrip("#")))


def make_frame(step: int) -> bytes:
    bg = rgb("171329")
    pixels = bytearray(bg * (WIDTH * HEIGHT))

    def point(x: int, y: int, color: str) -> None:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            i = (y * WIDTH + x) * 3
            pixels[i : i + 3] = bytes(rgb(color))

    def ellipse(cx: float, cy: float, rx: float, ry: float, color: str) -> None:
        for y in range(max(0, int(cy - ry)), min(HEIGHT, int(cy + ry + 1))):
            for x in range(max(0, int(cx - rx)), min(WIDTH, int(cx + rx + 1))):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    point(x, y, color)

    def polygon(vertices: list[tuple[int, int]], color: str) -> None:
        for y in range(max(0, min(p[1] for p in vertices)), min(HEIGHT, max(p[1] for p in vertices) + 1)):
            crosses = []
            for a, b in zip(vertices, vertices[1:] + vertices[:1]):
                if (a[1] <= y < b[1]) or (b[1] <= y < a[1]):
                    crosses.append(a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
            crosses.sort()
            for left, right in zip(crosses[::2], crosses[1::2]):
                for x in range(max(0, math.ceil(left)), min(WIDTH, math.floor(right) + 1)):
                    point(x, y, color)

    def stroke(x1: float, y1: float, x2: float, y2: float, radius: int, color: str) -> None:
        distance = max(1, int(math.hypot(x2 - x1, y2 - y1) * 2))
        for n in range(distance + 1):
            t = n / distance
            ellipse(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, radius, radius, color)

    def sparkle(x: int, y: int, scale: int = 1) -> None:
        stroke(x - 5 * scale, y, x + 5 * scale, y, scale, "F5D89B")
        stroke(x, y - 5 * scale, x, y + 5 * scale, scale, "F5D89B")
        ellipse(x, y, 2 * scale, 2 * scale, "FFF4CE")

    # A night-sky card frames the character, with stars that gently twinkle.
    ellipse(160, 109, 130, 92, "211B38")
    ellipse(160, 109, 103, 79, "2D2445")
    for n, (x, y) in enumerate([(38, 40), (278, 33), (268, 133), (47, 153), (106, 24), (220, 181)]):
        if (step + n * 3) % 16 < 13:
            sparkle(x, y, 1 if n % 2 else 2)
    ellipse(160, 197, 86, 12, "100D1E")

    # Tail, body, and two moving paws sit behind the face.
    ellipse(227, 159, 36, 22, "A18BBE")
    ellipse(219, 149, 27, 19, "CCB9E5")
    ellipse(160, 148, 66, 57, "A18BBE")
    ellipse(160, 143, 59, 52, "D3C3EA")
    phase = math.sin(step * math.tau / 16)
    paws = [(105, 118, 68 + 12 * phase, 82 - 12 * phase),
            (215, 118, 252 - 12 * phase, 82 + 12 * phase)]
    for shoulder_x, shoulder_y, x, y in paws:
        stroke(shoulder_x, shoulder_y, x, y, 15, "A18BBE")
        stroke(shoulder_x, shoulder_y, x, y, 12, "D3C3EA")
        ellipse(x, y, 20, 18, "A18BBE")
        ellipse(x, y - 2, 17, 15, "E2D5F2")
        ellipse(x, y - 1, 7, 5, "EAB3BE")
        for pad_x in (-8, 0, 8):
            ellipse(x + pad_x, y - 10, 2, 3, "EAB3BE")

    # Pointed ears and soft round face.
    polygon([(101, 86), (103, 36), (136, 58)], "A18BBE")
    polygon([(219, 86), (217, 36), (184, 58)], "A18BBE")
    polygon([(108, 76), (110, 47), (131, 62)], "EAB3BE")
    polygon([(212, 76), (210, 47), (189, 62)], "EAB3BE")
    ellipse(160, 96, 64, 54, "A18BBE")
    ellipse(160, 92, 59, 50, "E2D5F2")
    ellipse(136, 90, 8, 12, "20182F")
    ellipse(184, 90, 8, 12, "20182F")
    ellipse(139, 85, 3, 4, "FFF9F1")
    ellipse(187, 85, 3, 4, "FFF9F1")
    ellipse(123, 109, 11, 6, "EAB3BE")
    ellipse(197, 109, 11, 6, "EAB3BE")
    ellipse(148, 112, 15, 10, "FFF3F1")
    ellipse(172, 112, 15, 10, "FFF3F1")
    polygon([(153, 106), (167, 106), (160, 114)], "8C627E")
    stroke(160, 113, 156, 120, 1, "8C627E")
    stroke(160, 113, 164, 120, 1, "8C627E")
    for y in (106, 114):
        stroke(135, y, 103, y - 5, 1, "B5A2CC")
        stroke(185, y, 217, y - 5, 1, "B5A2CC")

    # A small golden bow makes the cat fit the fantasy-game profile.
    polygon([(160, 145), (137, 134), (141, 157)], "D9AE69")
    polygon([(160, 145), (183, 134), (179, 157)], "D9AE69")
    ellipse(160, 145, 7, 7, "FFF0C7")
    for x in (133, 187):
        ellipse(x, 188, 21, 9, "A18BBE")
        ellipse(x, 185, 19, 8, "E2D5F2")

    # A floating heart bobs with the wave.
    hy = 48 + round(3 * math.sin(step * math.tau / 16))
    ellipse(250, hy, 5, 5, "EAB3BE")
    ellipse(258, hy, 5, 5, "EAB3BE")
    polygon([(245, hy + 1), (263, hy + 1), (254, hy + 13)], "EAB3BE")
    return bytes(pixels)


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    for step in range(16):
        path = FRAMES / f"frame_{step:02}.ppm"
        with path.open("wb") as file:
            file.write(f"P6\n{WIDTH} {HEIGHT}\n255\n".encode())
            file.write(make_frame(step))
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-framerate", "10", "-i",
         str(FRAMES / "frame_%02d.ppm"), "-filter_complex",
         "split[a][b];[a]palettegen[p];[b][p]paletteuse", "-loop", "0", str(OUTPUT)],
        check=True,
    )
    shutil.rmtree(FRAMES)
    print(f"Created {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
