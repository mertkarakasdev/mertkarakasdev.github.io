# -*- coding: utf-8 -*-
"""Favicon dosyalarını sıfırdan üretir (harici bağımlılık yok).
Renk/şekil değiştirmek için aşağıdaki sabitleri düzenleyip çalıştır:
    python3 scripts/favicon.py
"""
import zlib, struct, pathlib

ZEMIN = (27, 31, 36)      # #1b1f24
HARF  = (245, 246, 247)   # #f5f6f7
KOSE  = 0.18              # köşe yuvarlaklığı (kenarın oranı)
ORNEK = 4                 # süper örnekleme (kenar yumuşatma)

CIKTI = pathlib.Path(__file__).resolve().parent.parent / "static"


def _mesafe(px, py, ax, ay, bx, by):
    """Noktanın AB doğru parçasına uzaklığı."""
    dx, dy = bx - ax, by - ay
    uzunluk = dx * dx + dy * dy
    t = 0.0 if uzunluk == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / uzunluk))
    return ((px - (ax + t * dx)) ** 2 + (py - (ay + t * dy)) ** 2) ** 0.5


def _harf_icinde(x, y):
    """Normalize (0..1) koordinat M harfinin içinde mi?"""
    kalinlik = 0.062
    # iki dikey kol
    if 0.25 <= y <= 0.76 and (0.195 <= x <= 0.195 + 2 * kalinlik or
                              0.805 - 2 * kalinlik <= x <= 0.805):
        return True
    # iki çapraz
    if _mesafe(x, y, 0.257, 0.25, 0.50, 0.585) <= kalinlik:
        return True
    if _mesafe(x, y, 0.743, 0.25, 0.50, 0.585) <= kalinlik:
        return True
    return False


def _zemin_icinde(x, y):
    """Yuvarlatılmış kare."""
    r = KOSE
    cx = min(max(x, r), 1 - r)
    cy = min(max(y, r), 1 - r)
    return ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 <= r + 1e-9


def piksel_uret(boyut):
    satirlar = []
    for sy in range(boyut):
        satir = []
        for sx in range(boyut):
            zemin_say = harf_say = 0
            for ay in range(ORNEK):
                for ax in range(ORNEK):
                    x = (sx + (ax + 0.5) / ORNEK) / boyut
                    y = (sy + (ay + 0.5) / ORNEK) / boyut
                    if _zemin_icinde(x, y):
                        zemin_say += 1
                        if _harf_icinde(x, y):
                            harf_say += 1
            toplam = ORNEK * ORNEK
            if zemin_say == 0:
                satir.append((0, 0, 0, 0))
                continue
            k = harf_say / zemin_say                      # harf kaplama oranı
            renk = tuple(round(ZEMIN[i] + (HARF[i] - ZEMIN[i]) * k) for i in range(3))
            satir.append(renk + (round(255 * zemin_say / toplam),))
        satirlar.append(satir)
    return satirlar


def png(boyut):
    ham = b"".join(b"\x00" + bytes(d for p in satir for d in p) for satir in piksel_uret(boyut))

    def parca(tur, veri):
        g = tur + veri
        return struct.pack(">I", len(veri)) + g + struct.pack(">I", zlib.crc32(g) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n"
            + parca(b"IHDR", struct.pack(">IIBBBBB", boyut, boyut, 8, 6, 0, 0, 0))
            + parca(b"IDAT", zlib.compress(ham, 9))
            + parca(b"IEND", b""))


def ico(png_verisi, boyut):
    """Tek PNG'yi ICO kabuğuna sarar."""
    baslik = struct.pack("<HHH", 0, 1, 1)
    giris = struct.pack("<BBBBHHII", boyut if boyut < 256 else 0, boyut if boyut < 256 else 0,
                        0, 0, 1, 32, len(png_verisi), 22)
    return baslik + giris + png_verisi


def svg_maske():
    """Safari pinned tab: tek renkli siluet."""
    n = 64
    yollar = []
    for sy in range(n):
        bas = None
        for sx in range(n + 1):
            ic = sx < n and _harf_icinde((sx + 0.5) / n, (sy + 0.5) / n)
            if ic and bas is None:
                bas = sx
            elif not ic and bas is not None:
                yollar.append(f"M{bas} {sy}h{sx - bas}v1h-{sx - bas}z")
                bas = None
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
            f'  <path d="{"".join(yollar)}"/>\n</svg>\n')


CIKTI.mkdir(exist_ok=True)
p32 = png(32)
(CIKTI / "favicon-16x16.png").write_bytes(png(16))
(CIKTI / "favicon-32x32.png").write_bytes(p32)
(CIKTI / "apple-touch-icon.png").write_bytes(png(180))
(CIKTI / "favicon.ico").write_bytes(ico(p32, 32))
(CIKTI / "safari-pinned-tab.svg").write_text(svg_maske(), encoding="utf-8")
for f in sorted(CIKTI.iterdir()):
    print(f"{f.name:26} {f.stat().st_size:>7} byte")
