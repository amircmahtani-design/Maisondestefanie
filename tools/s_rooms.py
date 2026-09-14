# -*- coding: utf-8 -*-
"""The wider frames. None of them try to be a photograph of a room —
they are close, shallow, low-key still lifes, which is what the page is
built out of anyway."""
import math, random
from kit import (head, foot, texture, grain, bloom, dark, bottle, bokeh,
                 petal, FILTERS)

SEAL_DEFS = """
  <linearGradient id="bigGlass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#180A02"/>
    <stop offset=".05"  stop-color="#8A4E14"/>
    <stop offset=".14"  stop-color="#3A1C05"/>
    <stop offset=".44"  stop-color="#A2601F"/>
    <stop offset=".62"  stop-color="#6E3A0E"/>
    <stop offset=".82"  stop-color="#D9963F"/>
    <stop offset=".91"  stop-color="#F8DCA8"/>
    <stop offset="1"    stop-color="#2E1504"/>
  </linearGradient>
  <linearGradient id="deepen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="#000" stop-opacity=".6"/>
    <stop offset=".2"  stop-color="#000" stop-opacity=".12"/>
    <stop offset=".72" stop-color="#000" stop-opacity="0"/>
    <stop offset="1"   stop-color="#1A0800" stop-opacity=".55"/>
  </linearGradient>
  <radialGradient id="wax" cx=".36" cy=".26" r=".85">
    <stop offset="0"   stop-color="#B04252"/>
    <stop offset=".42" stop-color="#6E2333"/>
    <stop offset="1"   stop-color="#260A12"/>
  </radialGradient>"""

SHOP_DEFS = """
  <linearGradient id="win" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="#E8B76A" stop-opacity=".85"/>
    <stop offset=".55" stop-color="#C98A3A" stop-opacity=".7"/>
    <stop offset="1"   stop-color="#6E3C0E" stop-opacity=".55"/>
  </linearGradient>"""

WOOD = '''
  <linearGradient id="woodTop" x1=".1" y1="0" x2=".95" y2=".4">
    <stop offset="0"   stop-color="#0B0705"/>
    <stop offset=".42" stop-color="#1A1108"/>
    <stop offset=".72" stop-color="#2A1B0C"/>
    <stop offset="1"   stop-color="#0E0906"/>
  </linearGradient>
  <linearGradient id="airBack" x1=".1" y1="0" x2=".9" y2=".55">
    <stop offset="0"   stop-color="#080503"/>
    <stop offset=".48" stop-color="#120C07"/>
    <stop offset=".76" stop-color="#231708"/>
    <stop offset="1"   stop-color="#0B0705"/>
  </linearGradient>'''


# ══════════════════════════════════════════════════════════════════════
def hero_still(W=2400, H=1350):
    """The counter, seen wide. A candle off to the right does all of it."""
    rnd = random.Random(5)
    top = H * 0.72
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="url(#airBack)"/>
  {texture(W,H,'.0025 .008',5,4,'.30')}

  <!-- the source -->
  {bloom(W*0.745, H*0.30, 620, 520, '#C98A3A', '.30', 'b240')}
  {bloom(W*0.752, H*0.275, 210, 220, '#E8A94F', '.40', 'b60')}
  <rect x="{W*0.752-25:.0f}" y="{H*0.298:.0f}" width="50" height="168" rx="6" fill="#2E1F0E"/>
  <rect x="{W*0.752-25:.0f}" y="{H*0.298:.0f}" width="50" height="168" rx="6" fill="#8A6532" opacity=".45"/>
  <rect x="{W*0.752+2:.0f}" y="{H*0.300:.0f}" width="21" height="164" rx="9" fill="#F0D49A" opacity=".62" filter="url(#b4)"/>
  <rect x="{W*0.752-25:.0f}" y="{H*0.298:.0f}" width="18" height="168" fill="#120B05" opacity=".6"/>
  <ellipse cx="{W*0.752:.0f}" cy="{H*0.300:.0f}" rx="25" ry="7" fill="#E8C88A" opacity=".7" filter="url(#b2)"/>
  <ellipse cx="{W*0.752:.0f}" cy="{H*0.256:.0f}" rx="15" ry="33" fill="#FFDFA6" opacity=".8" filter="url(#b8)"/>
  <ellipse cx="{W*0.752:.0f}" cy="{H*0.250:.0f}" rx="6"  ry="18" fill="#FFF6E0" opacity=".95" filter="url(#b1)"/>

  <!-- three shelves of bottles receding, each further out of focus -->
  {''.join(bottle(W*0.30 + i*118, top-190, rnd.uniform(46,74), rnd.uniform(118,196),
                  key=max(.04, 1-abs(W*0.30+i*118 - W*0.74)/(W*0.62))*0.5,
                  blur='b16') for i in range(13))}
  <rect x="{W*0.22:.0f}" y="{top-192:.0f}" width="{W*0.72:.0f}" height="7" fill="#150E08" filter="url(#b8)"/>
  {''.join(bottle(W*0.36 + i*136, top-24, rnd.uniform(58,92), rnd.uniform(150,250),
                  key=max(.05, 1-abs(W*0.36+i*136 - W*0.74)/(W*0.58)),
                  blur='b8', hue=rnd.choice(['amber','amber','smoke','green']),
                  label=rnd.random()<.4) for i in range(9))}
  {bokeh(rnd, 20, W*0.34, W*0.99, H*0.06, H*0.60, 14, 52)}

  <!-- the counter -->
  <rect x="0" y="{top:.0f}" width="{W}" height="{H-top:.0f}" fill="url(#woodTop)"/>
  {texture(W,H,'.0015 .07',4,9,'.22')}
  <rect x="0" y="{top:.0f}" width="{W}" height="3" fill="#A8804A" opacity=".4" filter="url(#b2)"/>
  {bloom(W*0.72, top+70, 660, 96, '#B8761F', '.28', 'b120')}
  {''.join(f'<ellipse cx="{W*0.36+i*136:.0f}" cy="{top+40:.0f}" rx="30" ry="52" fill="#C98A3A" '
           f'opacity=".07" filter="url(#b30)" style="mix-blend-mode:screen"/>' for i in range(9))}

  <!-- the left half is not lit at all -->
  {dark(W*0.02, H*0.52, 800, 1000, '.9', 'b240')}
  {dark(W*0.24, H*0.18, 620, 500, '.5', 'b240')}
{foot(W,H)}'''


# ══════════════════════════════════════════════════════════════════════
def workshop(W=2400, H=1030):
    """Her essences, close and shallow — a row of glass at eye level."""
    rnd = random.Random(19)
    base = H * 0.86
    out = []
    # back row, well out of focus
    for i in range(16):
        x = W*0.05 + i*152 + rnd.uniform(-16, 16)
        out.append(bottle(x, base-118, rnd.uniform(44, 74), rnd.uniform(96, 168),
                          key=max(.03, 1-abs(x-W*0.70)/(W*0.62))*0.45, blur='b30',
                          hue=rnd.choice(['amber', 'smoke', 'green'])))
    out.append(f'<rect x="0" y="{base-120:.0f}" width="{W}" height="9" fill="#120C07" filter="url(#b16)"/>')
    # middle row, softly off
    for i in range(11):
        x = W*0.03 + i*228 + rnd.uniform(-20, 20)
        out.append(bottle(x, base-16, rnd.uniform(70, 118), rnd.uniform(180, 290),
                          key=max(.05, 1-abs(x-W*0.70)/(W*0.58))*0.85, blur='b8',
                          hue=rnd.choice(['amber', 'amber', 'smoke'])))
    # the two in focus, right where the light is
    out.append(bottle(W*0.655, base, 168, 396, key=1.0, hue='amber', label=True))
    out.append(bottle(W*0.775, base, 132, 322, key=.9, hue='smoke', label=True))
    out.append(bottle(W*0.55, base, 104, 268, key=.6, blur='b4', hue='green'))
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="url(#airBack)"/>
  {texture(W,H,'.003 .009',5,12,'.28')}
  {bloom(W*0.70, H*0.36, 720, 560, '#C98A3A', '.30', 'b240')}
  {bloom(W*0.72, H*0.30, 250, 240, '#E8A94F', '.26', 'b60')}
  {''.join(out)}
  <rect x="0" y="{base:.0f}" width="{W}" height="{H-base:.0f}" fill="url(#woodTop)"/>
  <rect x="0" y="{base:.0f}" width="{W}" height="3" fill="#A8804A" opacity=".35" filter="url(#b2)"/>
  {bloom(W*0.70, base+40, 620, 70, '#B8761F', '.26', 'b120')}
  {bokeh(rnd, 18, W*0.38, W*0.99, H*0.04, H*0.8, 12, 46)}
  {dark(W*0.0, H*0.5, 470, 820, '.7', 'b240')}
  {dark(W*1.0, H*0.5, 300, 620, '.42', 'b240')}
{foot(W,H,'.05',14)}'''


# ══════════════════════════════════════════════════════════════════════
def atwork(W=2400, H=1030):
    """The whole counter in one wide frame: the bowl, the petals, the
       glass, and a long rake of light across the wood."""
    rnd = random.Random(29)
    top = H * 0.40
    bx, by = W*0.60, H*0.86
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="url(#airBack)"/>
  {texture(W,H,'.003 .008',5,31,'.26')}
  {bloom(W*0.76, H*0.18, 640, 460, '#C98A3A', '.30', 'b240')}

  <!-- a wall of shelving thrown right out of focus -->
  {''.join(bottle(W*0.04 + i*140, top-14, rnd.uniform(40,72), rnd.uniform(90,170),
                  key=max(.03, 1-abs(W*0.04+i*140 - W*0.76)/(W*0.7))*0.4, blur='b30',
                  hue=rnd.choice(['amber','smoke','green'])) for i in range(16))}
  <rect x="0" y="{top-16:.0f}" width="{W}" height="8" fill="#100B06" filter="url(#b16)"/>

  <!-- the counter, raking away to the left -->
  <rect x="0" y="{top+70:.0f}" width="{W}" height="{H-top-70:.0f}" fill="url(#woodTop)"/>
  {texture(W,H,'.0012 .06',4,44,'.24')}
  <rect x="0" y="{top+70:.0f}" width="{W}" height="3" fill="#A8804A" opacity=".4" filter="url(#b2)"/>
  {bloom(W*0.74, top+230, 760, 150, '#B8761F', '.30', 'b120')}

  <!-- the bowl -->
  <g>
    <ellipse cx="{bx:.0f}" cy="{by-6:.0f}" rx="200" ry="30" fill="#000" opacity=".8" filter="url(#b30)"/>
    <path d="M{bx-210:.0f} {by-190:.0f} C {bx-210:.0f} {by-40:.0f} {bx-110:.0f} {by:.0f} {bx:.0f} {by:.0f}
             C {bx+110:.0f} {by:.0f} {bx+210:.0f} {by-40:.0f} {bx+210:.0f} {by-190:.0f} Z"
          fill="#1E1206" opacity=".8"/>
    <path d="M{bx-190:.0f} {by-176:.0f} C {bx-190:.0f} {by-52:.0f} {bx-100:.0f} {by-14:.0f} {bx:.0f} {by-14:.0f}
             C {bx+100:.0f} {by-14:.0f} {bx+190:.0f} {by-52:.0f} {bx+190:.0f} {by-176:.0f} Z"
          fill="#7A4412" opacity=".8"/>
    <ellipse cx="{bx:.0f}" cy="{by-186:.0f}" rx="192" ry="40" fill="#C4832C"/>
    <ellipse cx="{bx+48:.0f}" cy="{by-196:.0f}" rx="76" ry="14" fill="#FFEAC4" opacity=".55" filter="url(#b8)"/>
    <ellipse cx="{bx:.0f}" cy="{by-190:.0f}" rx="210" ry="44" fill="none"
             stroke="#6E5A38" stroke-width="2.5" opacity=".55"/>
    <path d="M{bx-30:.0f} {by-232:.0f} A 210 44 0 0 1 {bx+200:.0f} {by-198:.0f}"
          stroke="#FFFDF6" stroke-width="6" fill="none" opacity=".85" filter="url(#b2)"/>
    <path d="M{bx+204:.0f} {by-172:.0f} C {bx+204:.0f} {by-56:.0f} {bx+120:.0f} {by-18:.0f} {bx+66:.0f} {by-14:.0f}"
          stroke="#FFF2D8" stroke-width="7" fill="none" opacity=".5" filter="url(#b4)" stroke-linecap="round"/>
  </g>

  <!-- glass to the right of it, and petals across the wood -->
  {bottle(W*0.845, by, 150, 356, key=1.0, hue='amber', label=True)}
  {bottle(W*0.925, by, 104, 244, key=.7, blur='b4', hue='smoke')}
  {''.join(petal(rnd.uniform(W*0.20, W*0.56), rnd.uniform(H*0.74, H*0.97),
                 rnd.uniform(26,52), rnd.uniform(0,360),
                 key=max(.06, 1-abs(rnd.uniform(W*0.20,W*0.56)-W*0.7)/(W*0.6)))
           for _ in range(9))}
  {bokeh(rnd, 16, W*0.42, W*0.99, H*0.02, H*0.6, 12, 48)}
  {dark(W*0.0, H*0.5, 480, 820, '.72', 'b240')}
{foot(W,H,'.05',19)}'''


# ══════════════════════════════════════════════════════════════════════
def counter_panel(W=900, H=1125):
    """A pipette over blotting strips."""
    rnd = random.Random(41)
    strips = []
    for i in range(6):
        a = -56 + i*15 + rnd.uniform(-4, 4)
        L = rnd.uniform(300, 430)
        k = max(0.08, 1 - abs(i-4)/5)
        strips.append(f'''<g transform="translate({W*0.42:.0f},{H*0.72:.0f}) rotate({a:.0f})">
      <rect x="-14" y="-{L:.0f}" width="28" height="{L:.0f}" rx="2" fill="#000" opacity=".55"
            transform="translate(5,7)" filter="url(#b8)"/>
      <rect x="-14" y="-{L:.0f}" width="28" height="{L:.0f}" rx="2" fill="#2A1C0C"/>
      <rect x="-14" y="-{L:.0f}" width="28" height="{L:.0f}" rx="2" fill="#D8B279" opacity="{0.18+k*0.7:.2f}"/>
      <rect x="-14" y="-{L:.0f}" width="11" height="{L:.0f}" fill="#0A0604" opacity=".38"/>
      <ellipse cx="0" cy="-{L*0.9:.0f}" rx="13" ry="24" fill="#8A5A1E" opacity="{0.2+k*0.4:.2f}" filter="url(#b8)"/>
    </g>''')
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="url(#woodTop)"/>
  {texture(W,H,'.0018 .05',5,7,'.30')}
  {bloom(W*0.70, H*0.22, 460, 440, '#C98A3A', '.32', 'b120')}
  <ellipse cx="{W*0.42:.0f}" cy="{H*0.74:.0f}" rx="250" ry="96" fill="#000" opacity=".5" filter="url(#b60)"/>
  {''.join(strips)}

  <g transform="translate({W*0.63:.0f},{H*0.38:.0f}) rotate(26)">
    <rect x="-8" y="-320" width="16" height="500" rx="8" fill="#000" opacity=".6"
          transform="translate(8,10)" filter="url(#b8)"/>
    <rect x="-8" y="-320" width="16" height="500" rx="8" fill="#120C07"/>
    <rect x="-8" y="-320" width="16" height="500" rx="8" fill="#4A3A20" opacity=".65"/>
    <rect x="2" y="-316" width="4" height="492" rx="2" fill="#FFEBC4" opacity=".8" filter="url(#b1)"/>
    <rect x="-6" y="66" width="12" height="112" rx="6" fill="#B8761F" opacity=".9"/>
    <rect x="-10" y="-352" width="20" height="56" rx="9" fill="#241A0C"/>
    <rect x="-3" y="-348" width="4" height="48" rx="2" fill="#D9B36A" opacity=".5"/>
  </g>
  <ellipse cx="{W*0.775:.0f}" cy="{H*0.575:.0f}" rx="8" ry="12" fill="#F0BE74" opacity=".95" filter="url(#b1)"/>
  {bloom(W*0.775, H*0.575, 70, 70, '#E8A94F', '.42', 'b16')}

  {bottle(W*0.16, H*0.52, 168, 356, key=.35, blur='b30', hue='amber')}
  {bokeh(rnd, 8, W*0.05, W*0.95, H*0.03, H*0.45, 14, 46)}
  {dark(W*0.0, H*0.6, 320, 620, '.72', 'b120')}
{foot(W,H,'.055',22)}'''


# ══════════════════════════════════════════════════════════════════════
def botanical_panel(W=900, H=1125):
    """Petals, resin and mastic on stone, under a raking light."""
    rnd = random.Random(53)
    bits = []
    for _ in range(15):
        x, y = rnd.uniform(W*0.14, W*0.90), rnd.uniform(H*0.36, H*0.94)
        k = max(0.06, 1 - math.hypot(x-W*0.70, y-H*0.30)/(W*1.05))
        bits.append(petal(x, y, rnd.uniform(30, 62), rnd.uniform(0, 360), key=k))
    for _ in range(14):
        x, y = rnd.uniform(W*0.12, W*0.90), rnd.uniform(H*0.30, H*0.96)
        r = rnd.uniform(12, 30)
        k = max(0.08, 1 - math.hypot(x-W*0.70, y-H*0.30)/(W*1.05))
        bits.append(f'''<g transform="translate({x:.0f},{y:.0f})">
      <ellipse cx="3" cy="5" rx="{r*1.2:.0f}" ry="{r*0.6:.0f}" fill="#000" opacity=".6" filter="url(#b8)"/>
      <circle r="{r:.0f}" fill="#3A2A0E"/>
      <circle r="{r:.0f}" fill="#B8873A" opacity="{0.16+k*0.62:.2f}"/>
      <ellipse cx="{r*0.3:.0f}" cy="{-r*0.34:.0f}" rx="{r*0.3:.0f}" ry="{r*0.22:.0f}"
               fill="#FFF0CC" opacity="{0.1+k*0.7:.2f}" filter="url(#b1)"/>
    </g>''')
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="#0C0906"/>
  <rect width="{W}" height="{H}" fill="url(#airBack)" opacity=".9"/>
  {texture(W,H,'.006 .007',6,15,'.34')}
  {bloom(W*0.72, H*0.16, 470, 420, '#C98A3A', '.34', 'b120')}
  {''.join(bits)}
  {dark(W*0.02, H*0.72, 400, 620, '.78', 'b120')}
  {dark(W*0.5, H*1.02, 620, 260, '.6', 'b120')}
{foot(W,H,'.065',27)}'''


# ══════════════════════════════════════════════════════════════════════
def bench_panel(W=900, H=1125):
    """The bench with the lamp on: the card she writes the formula on,
       the small bottles, the brass. No one in the frame."""
    rnd = random.Random(61)
    top = H*0.56
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="url(#airBack)"/>
  {texture(W,H,'.0025 .009',5,33,'.28')}
  {bloom(W*0.76, H*0.05, 470, 400, '#C98A3A', '.36', 'b120')}
  <path d="M{W*0.58:.0f} 0 L{W*1.02:.0f} 0 L{W*1.06:.0f} {H*0.72:.0f} L{W*0.30:.0f} {H*0.78:.0f} Z"
        fill="#C98A3A" opacity=".09" filter="url(#b60)" style="mix-blend-mode:screen"/>

  <!-- shelf behind -->
  {''.join(bottle(W*0.06 + i*104, top-70, rnd.uniform(40,64), rnd.uniform(80,148),
                  key=max(.04, 1-abs(W*0.06+i*104 - W*0.78)/(W*0.72))*0.55, blur='b16',
                  hue=rnd.choice(['amber','smoke'])) for i in range(9))}
  <rect x="0" y="{top-72:.0f}" width="{W}" height="7" fill="#120C07" filter="url(#b8)"/>

  <!-- the bench -->
  <rect x="0" y="{top:.0f}" width="{W}" height="{H-top:.0f}" fill="url(#woodTop)"/>
  {texture(W,H,'.0015 .06',4,71,'.24')}
  <rect x="0" y="{top:.0f}" width="{W}" height="3" fill="#A8804A" opacity=".4" filter="url(#b2)"/>
  {bloom(W*0.72, top+90, 420, 110, '#B8761F', '.28', 'b120')}

  <!-- the card, written on by hand -->
  <g transform="translate({W*0.40:.0f},{top+188:.0f}) rotate(-7)">
    <rect x="-186" y="-118" width="372" height="236" rx="3" fill="#000" opacity=".6"
          transform="translate(9,14)" filter="url(#b16)"/>
    <rect x="-186" y="-118" width="372" height="236" rx="3" fill="#C6B694"/>
    <rect x="-186" y="-118" width="372" height="236" rx="3" fill="#F0E6CC" opacity=".55"/>
    <rect x="-186" y="-118" width="176" height="236" fill="#0A0604" opacity=".24"/>
    <rect x="-160" y="-92" width="320" height="184" rx="1" fill="none" stroke="#8A7350" stroke-width="1" opacity=".45"/>
    {''.join(f'<rect x="-140" y="{-64+i*30}" width="{rnd.uniform(70,268):.0f}" height="4" rx="2" fill="#4A3A24" opacity="{0.30+0.16*i:.2f}"/>' for i in range(6))}
  </g>

  <!-- small bottles across the front, the nearest in focus -->
  {''.join(bottle(W*0.10 + i*86, top+56, rnd.uniform(34,54), rnd.uniform(66,124),
                  key=max(.08, 1-abs(W*0.10+i*86 - W*0.76)/(W*0.7)),
                  blur=None, hue='amber') for i in range(4))}
  {bottle(W*0.83, top+300, 132, 300, key=1.0, hue='amber', label=True)}

  <!-- brass -->
  <g transform="translate({W*0.72:.0f},{top+18:.0f})">
    <rect x="-62" y="-16" width="124" height="16" rx="4" fill="#2A1F0C"/>
    <rect x="-62" y="-16" width="124" height="3" rx="1.5" fill="#D9B36A" opacity=".55" filter="url(#b1)"/>
    <rect x="-5" y="-86" width="10" height="72" fill="#2A1F0C"/>
    <rect x="-2" y="-86" width="3" height="72" fill="#E8C88A" opacity=".5"/>
    <ellipse cx="0" cy="-90" rx="54" ry="8" fill="#3A2C12"/>
    <ellipse cx="0" cy="-93" rx="54" ry="8" fill="#C6A45C" opacity=".72"/>
    <ellipse cx="16" cy="-95" rx="20" ry="3" fill="#FFEEC4" opacity=".6" filter="url(#b1)"/>
  </g>
  {bokeh(rnd, 9, W*0.3, W*0.98, H*0.04, H*0.5, 14, 44)}
  {dark(W*0.0, H*0.58, 340, 660, '.76', 'b120')}
{foot(W,H,'.055',35)}'''


# ══════════════════════════════════════════════════════════════════════
def sealing_panel(W=900, H=1125):
    """A finished bottle, the cord and the wax, close in."""
    base = H*0.86
    return f'''{head(W,H,WOOD + SEAL_DEFS)}
  <rect width="{W}" height="{H}" fill="url(#airBack)"/>
  {texture(W,H,'.002 .05',5,44,'.28')}
  {bloom(W*0.76, H*0.16, 460, 420, '#C98A3A', '.34', 'b120')}
  <ellipse cx="{W*0.5:.0f}" cy="{base+16:.0f}" rx="250" ry="42" fill="#000" opacity=".8" filter="url(#b60)"/>
  <ellipse cx="{W*0.58:.0f}" cy="{base+8:.0f}" rx="170" ry="26" fill="#C98A3A" opacity=".3"
           filter="url(#b30)" style="mix-blend-mode:screen"/>

  <rect x="{W*0.29:.0f}" y="{H*0.30:.0f}" width="{W*0.42:.0f}" height="{base-H*0.30:.0f}" rx="24"
        fill="url(#bigGlass)"/>
  <rect x="{W*0.29:.0f}" y="{H*0.30:.0f}" width="{W*0.42:.0f}" height="{base-H*0.30:.0f}" rx="24"
        fill="url(#deepen)"/>
  <path d="M{W*0.71-8:.0f} {H*0.34:.0f} L{W*0.71-8:.0f} {base-52:.0f}"
        stroke="#FFF6E4" stroke-width="6" opacity=".92" stroke-linecap="round" filter="url(#b1)"/>

  <rect x="{W*0.355:.0f}" y="{H*0.52:.0f}" width="{W*0.29:.0f}" height="{H*0.18:.0f}" rx="2" fill="#E4DAC2"/>
  <rect x="{W*0.355:.0f}" y="{H*0.52:.0f}" width="{W*0.29:.0f}" height="{H*0.18:.0f}" rx="2"
        fill="none" stroke="#9C8253" stroke-width="1.3" opacity=".7"/>
  <rect x="{W*0.355:.0f}" y="{H*0.52:.0f}" width="{W*0.145:.0f}" height="{H*0.18:.0f}"
        fill="#2A1B08" opacity=".26"/>
  <g font-family="Liberation Serif, DejaVu Serif, Georgia, serif" text-anchor="middle" fill="#43341F">
    <text x="{W*0.5:.0f}" y="{H*0.588:.0f}" font-size="22" letter-spacing="2">LA MAISON</text>
    <text x="{W*0.5:.0f}" y="{H*0.620:.0f}" font-size="22" letter-spacing="2">DE STEFANIE</text>
    <text x="{W*0.5:.0f}" y="{H*0.662:.0f}" font-size="11" letter-spacing="5" fill="#6B573A">ATHENS</text>
  </g>

  <rect x="{W*0.435:.0f}" y="{H*0.16:.0f}" width="{W*0.13:.0f}" height="{H*0.15:.0f}" rx="7" fill="#6E3C0E"/>
  <rect x="{W*0.435:.0f}" y="{H*0.16:.0f}" width="{W*0.045:.0f}" height="{H*0.15:.0f}" fill="#1E0D02" opacity=".65"/>
  <rect x="{W*0.545:.0f}" y="{H*0.165:.0f}" width="6" height="{H*0.14:.0f}" fill="#FFE7BE" opacity=".6" filter="url(#b1)"/>
  <path d="M{W*0.435:.0f} {H*0.238:.0f} q {W*0.065:.0f} 28 {W*0.13:.0f} 0"
        stroke="#4A3720" stroke-width="8" fill="none"/>
  <path d="M{W*0.435:.0f} {H*0.236:.0f} q {W*0.065:.0f} 28 {W*0.13:.0f} 0"
        stroke="#8A7048" stroke-width="2.5" fill="none" opacity=".6"/>

  <g transform="translate({W*0.50:.0f},{H*0.19:.0f})">
    <ellipse cx="5" cy="10" rx="76" ry="36" fill="#000" opacity=".6" filter="url(#b8)"/>
    <path d="M-68 8 C -80 -32 -34 -50 4 -46 C 46 -42 78 -22 70 10 C 62 38 22 48 -10 44 C -46 40 -62 32 -68 8 Z"
          fill="url(#wax)"/>
    <path d="M-42 -20 C -20 -34 22 -34 40 -16" stroke="#D9788A" stroke-width="5" fill="none"
          opacity=".38" filter="url(#b1)"/>
    <circle r="22" fill="none" stroke="#2A0A12" stroke-width="3" opacity=".65"/>
    <text x="0" y="9" font-family="Liberation Serif, Georgia, serif" font-size="26"
          text-anchor="middle" fill="#38101C" opacity=".9">LS</text>
  </g>
  {dark(W*0.0, H*0.6, 320, 680, '.78', 'b120')}
{foot(W,H,'.055',41)}'''.replace('#260A12', '#260A12')


# ══════════════════════════════════════════════════════════════════════
def shopfront(W=900, H=1125):
    """The door from across the street: a warm window in a dark wall,
       shot wide open so the street in front is only light."""
    rnd = random.Random(83)
    wall_t, wall_b = H*0.10, H*0.80
    win_x, win_y, win_w, win_h = W*0.24, H*0.36, W*0.32, H*0.30
    return f'''{head(W,H,WOOD + SHOP_DEFS)}
  <rect width="{W}" height="{H}" fill="#070504"/>
  <!-- the wall, catching a little of its own window -->
  <rect x="0" y="{wall_t:.0f}" width="{W}" height="{wall_b-wall_t:.0f}" fill="#151009"/>
  {texture(W,H,'.005 .006',6,55,'.34')}
  {bloom(W*0.42, H*0.52, 420, 380, '#C98A3A', '.26', 'b240')}

  <!-- the window -->
  <rect x="{win_x-11:.0f}" y="{win_y-11:.0f}" width="{win_w+22:.0f}" height="{win_h+22:.0f}"
        rx="3" fill="#0A0705"/>
  <rect x="{win_x:.0f}" y="{win_y:.0f}" width="{win_w:.0f}" height="{win_h:.0f}" fill="url(#win)"/>
  <!-- glass and what stands behind it -->
  {''.join(f'<rect x="{win_x+win_w*0.08+i*win_w*0.20:.0f}" y="{win_y+win_h*0.44:.0f}" '
           f'width="{rnd.uniform(15,25):.0f}" height="{rnd.uniform(52,104):.0f}" rx="6" '
           f'fill="#2E1806" opacity=".78"/>' for i in range(4))}
  <rect x="{win_x:.0f}" y="{win_y+win_h*0.40:.0f}" width="{win_w:.0f}" height="5" fill="#2A1708" opacity=".7"/>
  <rect x="{win_x:.0f}" y="{win_y:.0f}" width="{win_w:.0f}" height="{win_h:.0f}"
        fill="none" stroke="#120C07" stroke-width="10"/>
  <line x1="{win_x+win_w*0.5:.0f}" y1="{win_y:.0f}" x2="{win_x+win_w*0.5:.0f}"
        y2="{win_y+win_h:.0f}" stroke="#120C07" stroke-width="7"/>
  {bloom(win_x+win_w*0.5, win_y+win_h*0.5, 230, 220, '#E8A94F', '.34', 'b60')}

  <!-- the door, standing open -->
  <rect x="{W*0.63:.0f}" y="{H*0.38:.0f}" width="{W*0.15:.0f}" height="{H*0.42:.0f}" rx="3" fill="#0B0806"/>
  <rect x="{W*0.655:.0f}" y="{H*0.41:.0f}" width="{W*0.10:.0f}" height="{H*0.30:.0f}"
        fill="#D9963F" opacity=".62" filter="url(#b8)"/>
  {bloom(W*0.705, H*0.56, 200, 230, '#E8A94F', '.32', 'b60')}

  <!-- the lamp above the door -->
  <rect x="{W*0.815:.0f}" y="{H*0.22:.0f}" width="4" height="{H*0.08:.0f}" fill="#1C1409"/>
  <path d="M{W*0.79:.0f} {H*0.315:.0f} L{W*0.845:.0f} {H*0.315:.0f} L{W*0.832:.0f} {H*0.285:.0f} L{W*0.803:.0f} {H*0.285:.0f} Z"
        fill="#241A0C"/>
  <ellipse cx="{W*0.8175:.0f}" cy="{H*0.312:.0f}" rx="15" ry="11" fill="#FFE0AA" opacity=".92" filter="url(#b4)"/>
  {bloom(W*0.8175, H*0.312, 230, 220, '#FFC46A', '.42', 'b60')}

  <!-- the sign board -->
  <rect x="{W*0.22:.0f}" y="{H*0.255:.0f}" width="{W*0.42:.0f}" height="{H*0.052:.0f}" rx="2" fill="#0E0A06"/>
  <rect x="{W*0.22:.0f}" y="{H*0.255:.0f}" width="{W*0.42:.0f}" height="2" fill="#8A6B36" opacity=".5"/>
  <text x="{W*0.43:.0f}" y="{H*0.293:.0f}" font-family="Liberation Serif, Georgia, serif"
        font-size="17" letter-spacing="3.4" text-anchor="middle" fill="#B8934F"
        opacity=".9">LA MAISON DE STEFANIE</text>

  <!-- the step and the cobbles, wet with the window light -->
  <rect x="0" y="{wall_b:.0f}" width="{W}" height="{H-wall_b:.0f}" fill="#0A0706"/>
  {''.join(f'<ellipse cx="{rnd.uniform(0,W):.0f}" cy="{rnd.uniform(wall_b+8,H):.0f}" '
           f'rx="{rnd.uniform(18,38):.0f}" ry="{rnd.uniform(8,15):.0f}" fill="#2A1E12" '
           f'opacity="{rnd.uniform(.25,.7):.2f}" filter="url(#b2)"/>' for _ in range(52))}
  {bloom(W*0.42, wall_b+56, 330, 80, '#C98A3A', '.30', 'b60')}
  {bloom(W*0.70, wall_b+50, 230, 60, '#C98A3A', '.24', 'b60')}

  <!-- a little of the street thrown out of focus in front -->
  {bokeh(rnd, 9, 0, W, H*0.86, H, 26, 66, op=(0.03,0.10), f='b60')}
  {dark(W*0.0, H*0.5, 260, 720, '.7', 'b240')}
  {dark(W*1.0, H*0.78, 260, 420, '.5', 'b240')}
  {dark(W*0.5, H*0.0, 700, 200, '.7', 'b240')}
{foot(W,H,'.06',47)}'''


# ══════════════════════════════════════════════════════════════════════
def plaka_panel(W=900, H=1125):
    """The stepped street outside: whitewashed walls, one lamp, and the
       steps going up into the dark."""
    rnd = random.Random(97)
    steps = []
    y, d = H*1.02, 58
    for i in range(14):
        inset = i*22
        k = max(0.06, 0.55 - i*0.038)
        steps.append(f'<rect x="{inset:.0f}" y="{y:.0f}" width="{W-inset*2:.0f}" height="{d:.0f}" fill="#0E0A07"/>')
        steps.append(f'<rect x="{inset:.0f}" y="{y:.0f}" width="{W-inset*2:.0f}" height="{d*0.30:.0f}" '
                     f'fill="#4A3A22" opacity="{k*0.55:.2f}"/>')
        steps.append(f'<rect x="{inset:.0f}" y="{y:.0f}" width="{W-inset*2:.0f}" height="3" '
                     f'fill="#C69A55" opacity="{k:.2f}" filter="url(#b1)"/>')
        y -= d*(1-i*0.03); d *= 0.94
    return f'''{head(W,H,WOOD)}
  <rect width="{W}" height="{H}" fill="#070504"/>
  <!-- the two walls, closing in as the street climbs -->
  <path d="M0 0 L{W*0.30:.0f} {H*0.40:.0f} L{W*0.30:.0f} {H} L0 {H} Z" fill="#151009"/>
  <path d="M{W} 0 L{W*0.70:.0f} {H*0.40:.0f} L{W*0.70:.0f} {H} L{W} {H} Z" fill="#100B08"/>
  {texture(W,H,'.005 .006',6,66,'.36')}
  {bloom(W*0.34, H*0.42, 400, 460, '#C98A3A', '.26', 'b240')}

  {''.join(steps)}

  <!-- the lamp on the left wall -->
  <rect x="{W*0.215:.0f}" y="{H*0.20:.0f}" width="4" height="{H*0.07:.0f}" fill="#1A1309"/>
  <ellipse cx="{W*0.227:.0f}" cy="{H*0.285:.0f}" rx="13" ry="17" fill="#FFE0AA" opacity=".95" filter="url(#b4)"/>
  {bloom(W*0.227, H*0.285, 260, 270, '#FFC46A', '.46', 'b60')}
  <!-- what it puts on the wall beside it -->
  <path d="M{W*0.06:.0f} {H*0.20:.0f} L{W*0.30:.0f} {H*0.40:.0f} L{W*0.30:.0f} {H*0.74:.0f} L{W*0.02:.0f} {H*0.60:.0f} Z"
        fill="#C98A3A" opacity=".14" filter="url(#b60)" style="mix-blend-mode:screen"/>

  <!-- a doorway further up, still lit -->
  <rect x="{W*0.70:.0f}" y="{H*0.44:.0f}" width="{W*0.055:.0f}" height="{H*0.13:.0f}" fill="#0A0705"/>
  <rect x="{W*0.706:.0f}" y="{H*0.447:.0f}" width="{W*0.043:.0f}" height="{H*0.116:.0f}"
        fill="#D9963F" opacity=".62" filter="url(#b4)"/>
  {bloom(W*0.727, H*0.505, 165, 175, '#E8A94F', '.32', 'b60')}
  <!-- shuttered window opposite -->
  <rect x="{W*0.235:.0f}" y="{H*0.46:.0f}" width="{W*0.05:.0f}" height="{H*0.09:.0f}" fill="#0A0705"/>
  <rect x="{W*0.24:.0f}" y="{H*0.466:.0f}" width="{W*0.04:.0f}" height="{H*0.078:.0f}" fill="#241A0E"/>

  <!-- bougainvillea coming over the top of the wall -->
  {''.join(f'<circle cx="{rnd.uniform(W*0.0,W*0.38):.0f}" cy="{rnd.uniform(H*0.0,H*0.24):.0f}" '
           f'r="{rnd.uniform(12,34):.0f}" fill="#3A0D18" opacity="{rnd.uniform(.35,.8):.2f}" '
           f'filter="url(#b8)"/>' for _ in range(28))}
  {''.join(f'<circle cx="{rnd.uniform(W*0.03,W*0.34):.0f}" cy="{rnd.uniform(H*0.01,H*0.20):.0f}" '
           f'r="{rnd.uniform(6,17):.0f}" fill="#7C2232" opacity="{rnd.uniform(.25,.65):.2f}" '
           f'filter="url(#b4)"/>' for _ in range(20))}
  {''.join(f'<ellipse cx="{rnd.uniform(W*0.0,W*0.30):.0f}" cy="{rnd.uniform(H*0.02,H*0.26):.0f}" '
           f'rx="{rnd.uniform(10,26):.0f}" ry="{rnd.uniform(5,12):.0f}" fill="#1A2412" '
           f'opacity="{rnd.uniform(.3,.7):.2f}" transform="rotate({rnd.uniform(0,360):.0f} '
           f'{rnd.uniform(W*0.0,W*0.30):.0f} {rnd.uniform(H*0.02,H*0.26):.0f})" filter="url(#b4)"/>'
           for _ in range(16))}

  {dark(W*0.5, H*1.06, 700, 300, '.68', 'b240')}
  {dark(W*1.0, H*0.16, 380, 400, '.62', 'b240')}
  {dark(W*0.0, H*0.9, 300, 340, '.5', 'b240')}
{foot(W,H,'.06',53)}'''
