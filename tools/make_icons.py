"""English Trainer のアプリアイコンを生成する。

外部ライブラリなし（zlib と struct だけ）。ロゴと同じ引用符マークを、
ブランドの青地に白抜きで描く。距離関数 + スーパーサンプリングでアンチエイリアス。

    python tools/make_icons.py

出力: pwa/icon-192.png, pwa/icon-512.png, pwa/favicon-64.png
"""

import struct
import zlib
from pathlib import Path

Point = tuple[float, float]

# ロゴ SVG と同じ座標系 (viewBox 0 0 14 20)
SEGMENTS: list[tuple[Point, Point]] = [((4.7, 5.0), (2.9, 11.4)), ((11.1, 5.0), (9.3, 11.4))]
STROKE_R = 1.7  # stroke-width 3.4 の半径
MARK_W_RATIO = 0.46  # アイコン幅に対するマークの幅（maskable 安全域の内側）
BG = (0x2C, 0x4A, 0x9A)  # --blue
FG = (0xF6, 0xF5, 0xF2)  # --sheet
SS = 3  # スーパーサンプリング倍率

_xs = [p[0] for s in SEGMENTS for p in s]
_ys = [p[1] for s in SEGMENTS for p in s]
BOX = (min(_xs) - STROKE_R, min(_ys) - STROKE_R, max(_xs) + STROKE_R, max(_ys) + STROKE_R)
CX = (BOX[0] + BOX[2]) / 2.0
CY = (BOX[1] + BOX[3]) / 2.0
BOX_W = BOX[2] - BOX[0]


def dist_to_segment(px: float, py: float, a: Point, b: Point) -> float:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    denom = dx * dx + dy * dy
    t = 0.0 if denom == 0 else ((px - ax) * dx + (py - ay) * dy) / denom
    t = max(0.0, min(1.0, t))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


def render(size: int) -> list[bytes]:
    """size x size の RGB バイト列を返す。"""
    k = MARK_W_RATIO * size / BOX_W  # ローカル座標 -> ピクセル
    half = size / 2.0
    rows: list[bytes] = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            hits = 0
            for sy in range(SS):
                for sx in range(SS):
                    # ピクセル中心をローカル座標へ逆写像
                    px = (x + (sx + 0.5) / SS - half) / k + CX
                    py = (y + (sy + 0.5) / SS - half) / k + CY
                    for a, b in SEGMENTS:
                        if dist_to_segment(px, py, a, b) <= STROKE_R:
                            hits += 1
                            break
            a = hits / float(SS * SS)
            row += bytes(round(BG[i] + (FG[i] - BG[i]) * a) for i in range(3))
        rows.append(bytes(row))
    return rows


def png_bytes(rows: list[bytes], size: int) -> bytes:
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag: bytes, data: bytes) -> bytes:
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    return png


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "pwa"
    out.mkdir(parents=True, exist_ok=True)
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png"), (64, "favicon-64.png")):
        p = out / name
        p.write_bytes(png_bytes(render(size), size))
        print(f"{p}  ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
