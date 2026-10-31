"""tools/make_icons.py: ロゴの線からアイコンの PNG を作る。"""

import struct
import zlib

from make_icons import dist_to_segment, png_bytes, render


def test_distance_to_a_segment():
    assert dist_to_segment(0, 1, (0, 0), (2, 0)) == 1
    assert dist_to_segment(3, 0, (0, 0), (2, 0)) == 1  # 端より先は端からの距離
    assert dist_to_segment(1, 1, (1, 0), (1, 0)) == 1  # 長さ 0 の線


def test_render_returns_one_rgb_row_per_line():
    rows = render(8)
    assert len(rows) == 8
    assert all(len(r) == 8 * 3 for r in rows)


def test_png_is_valid_and_has_the_size():
    png = png_bytes(render(8), 8)
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    width, height = struct.unpack(">II", png[16:24])
    assert (width, height) == (8, 8)
    ihdr = png[12:29]
    assert struct.unpack(">I", png[29:33])[0] == zlib.crc32(ihdr) & 0xFFFFFFFF
