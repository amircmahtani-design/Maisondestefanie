# -*- coding: utf-8 -*-
"""The shelf. Every product is stood on the same backdrop, at the same
height, under the same light — which is exactly what the Studio's house
treatment does to her own photographs, so these sit in the same set."""
import math, random

# the house backdrop, straight out of config.js
TOP, BOT = '#EFE8E0', '#D8CCC3'
W = H = 1200
BASE = int(H * 0.90)          # where everything stands


def _head(seed=1):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bd" x1=".2" y1="0" x2=".8" y2="1">
    <stop offset="0"   stop-color="{TOP}"/>
    <stop offset=".55" stop-color="#E6DCD2"/>
    <stop offset="1"   stop-color="{BOT}"/>
  </linearGradient>
  <radialGradient id="key" cx=".36" cy=".18" r=".8">
    <stop offset="0"   stop-color="#FFFFFF" stop-opacity=".55"/>
    <stop offset="1"   stop-color="#FFFFFF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cast" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#4A3A2E" stop-opacity=".46"/>
    <stop offset=".55" stop-color="#4A3A2E" stop-opacity=".18"/>
    <stop offset="1"   stop-color="#4A3A2E" stop-opacity="0"/>
  </radialGradient>
  <filter id="p1" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="1.4"/></filter>
  <filter id="p4" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="p12" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="p30" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="30"/></filter>
  <filter id="pg{seed}"><feTurbulence type="fractalNoise" baseFrequency=".82" numOctaves="3" seed="{seed}"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#bd)"/>
<rect width="{W}" height="{H}" fill="url(#key)"/>'''


def _foot(seed=1):
    return f'''<g style="mix-blend-mode:overlay" opacity=".05">
  <rect width="{W}" height="{H}" filter="url(#pg{seed})"/></g>
</svg>'''


def _shadow(cx, w, squash=0.16):
    return (f'<ellipse cx="{cx+w*0.10:.0f}" cy="{BASE+10}" rx="{w*0.86:.0f}" '
            f'ry="{w*squash:.0f}" fill="url(#cast)"/>')


def _plate(cx, cy, w, h, lines, small='ATHENS', fs=None):
    fs = fs or max(11, w * 0.085)
    body = ''.join(
        f'<text x="{cx:.0f}" y="{cy - h*0.5 + h*0.34 + i*fs*1.35:.0f}" font-size="{fs:.0f}" '
        f'letter-spacing="{fs*0.10:.1f}">{t}</text>' for i, t in enumerate(lines))
    return f'''<g>
    <rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="2"
          fill="#F2EBDC"/>
    <rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="2"
          fill="none" stroke="#A8956E" stroke-width="1" opacity=".65"/>
    <g font-family="Liberation Serif, DejaVu Serif, Georgia, serif" text-anchor="middle" fill="#43341F">
      {body}
      <text x="{cx:.0f}" y="{cy + h*0.34:.0f}" font-size="{fs*0.62:.0f}"
            letter-spacing="{fs*0.34:.1f}" fill="#7A6544">{small}</text>
    </g>
    <rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w*0.34:.0f}" height="{h:.0f}"
          fill="#8A7A62" opacity=".10"/>
  </g>'''


# ── the flacon, in whatever colour ────────────────────────────────────
def flacon(hue='amber', h_frac=0.62, w_frac=0.34, lines=('LA MAISON', 'DE STEFANIE'), seed=1):
    ramps = {
        'amber': ('#3A1C05', '#8A4E14', '#C88132', '#F3D296'),
        'rose':  ('#3E1720', '#7E3040', '#B06070', '#EDC3CB'),
        'green': ('#16240F', '#3A5222', '#6E8C42', '#CBDFA0'),
        'smoke': ('#1A1512', '#3E342A', '#6E5E4C', '#D8CBB6'),
        'clear': ('#8A8272', '#B8B0A0', '#DAD3C4', '#FFFFFF'),
    }
    a, b, c, d = ramps.get(hue, ramps['amber'])
    bw, bh = W*w_frac, H*h_frac
    bx, bt = (W-bw)/2, BASE-bh
    cx = W/2
    return f'''{_head(seed)}
{_shadow(cx, bw)}
<defs>
  <linearGradient id="fg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="{a}"/>
    <stop offset=".07"  stop-color="{c}"/>
    <stop offset=".18"  stop-color="{a}"/>
    <stop offset=".46"  stop-color="{b}"/>
    <stop offset=".62"  stop-color="{c}"/>
    <stop offset=".78"  stop-color="{b}"/>
    <stop offset=".90"  stop-color="{d}"/>
    <stop offset="1"    stop-color="{a}"/>
  </linearGradient>
  <linearGradient id="fv" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="#000" stop-opacity=".45"/>
    <stop offset=".18" stop-color="#000" stop-opacity=".08"/>
    <stop offset=".78" stop-color="#000" stop-opacity="0"/>
    <stop offset="1"   stop-color="#000" stop-opacity=".38"/>
  </linearGradient>
  <radialGradient id="cap" cx=".62" cy=".30" r=".9">
    <stop offset="0"   stop-color="#F6E3BC"/>
    <stop offset=".22" stop-color="#D9BC86"/>
    <stop offset=".52" stop-color="#9C7B3E"/>
    <stop offset=".80" stop-color="#5C4520"/>
    <stop offset="1"   stop-color="#8A6C32"/>
  </radialGradient>
</defs>
<!-- neck -->
<rect x="{cx-bw*0.13:.0f}" y="{bt-bh*0.15:.0f}" width="{bw*0.26:.0f}" height="{bh*0.20:.0f}"
      rx="{bw*0.03:.0f}" fill="url(#fg)"/>
<rect x="{cx-bw*0.16:.0f}" y="{bt-bh*0.17:.0f}" width="{bw*0.32:.0f}" height="{bh*0.055:.0f}"
      rx="4" fill="#8A6C32"/>
<rect x="{cx-bw*0.16:.0f}" y="{bt-bh*0.17:.0f}" width="{bw*0.32:.0f}" height="{bh*0.02:.0f}"
      rx="3" fill="#F0DCAC" opacity=".7" filter="url(#p1)"/>
<!-- stopper -->
<circle cx="{cx:.0f}" cy="{bt-bh*0.255:.0f}" r="{bw*0.185:.0f}" fill="url(#cap)"/>
<ellipse cx="{cx+bw*0.07:.0f}" cy="{bt-bh*0.30:.0f}" rx="{bw*0.05:.0f}" ry="{bw*0.033:.0f}"
         fill="#FFFAEC" opacity=".9" transform="rotate(-22 {cx+bw*0.07:.0f} {bt-bh*0.30:.0f})" filter="url(#p1)"/>
<!-- body -->
<rect x="{bx:.0f}" y="{bt:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{bw*0.075:.0f}" fill="url(#fg)"/>
<rect x="{bx:.0f}" y="{bt:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{bw*0.075:.0f}" fill="url(#fv)"/>
<rect x="{bx+bw-9:.0f}" y="{bt+bh*0.07:.0f}" width="4" height="{bh*0.80:.0f}" rx="2"
      fill="#FFFFFF" opacity=".72" filter="url(#p1)"/>
<rect x="{bx+6:.0f}" y="{bt+bh*0.12:.0f}" width="3" height="{bh*0.66:.0f}" rx="1.5"
      fill="#FFFFFF" opacity=".26" filter="url(#p1)"/>
{_plate(cx, bt+bh*0.56, bw*0.62, bh*0.34, lines)}
{_foot(seed)}'''


# ── a tall dropper bottle, for the oils ───────────────────────────────
def dropper(seed=2, hue=('#3A2A10', '#7A5A22', '#B8933F', '#F0DCA8')):
    a, b, c, d = hue
    bw, bh = W*0.26, H*0.56
    bx, bt = (W-bw)/2, BASE-bh
    cx = W/2
    return f'''{_head(seed)}
{_shadow(cx, bw)}
<defs>
  <linearGradient id="dg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{a}"/><stop offset=".08" stop-color="{c}"/>
    <stop offset=".2" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/>
    <stop offset=".72" stop-color="{c}"/><stop offset=".9" stop-color="{d}"/>
    <stop offset="1" stop-color="{a}"/>
  </linearGradient>
</defs>
<rect x="{cx-bw*0.30:.0f}" y="{bt-bh*0.30:.0f}" width="{bw*0.60:.0f}" height="{bh*0.16:.0f}"
      rx="{bw*0.06:.0f}" fill="#2E2418"/>
<rect x="{cx-bw*0.30:.0f}" y="{bt-bh*0.30:.0f}" width="{bw*0.16:.0f}" height="{bh*0.16:.0f}"
      fill="#0E0A06" opacity=".45"/>
<rect x="{cx+bw*0.16:.0f}" y="{bt-bh*0.285:.0f}" width="{bw*0.06:.0f}" height="{bh*0.13:.0f}"
      rx="4" fill="#8A7A5E" opacity=".7" filter="url(#p1)"/>
<rect x="{cx-bw*0.12:.0f}" y="{bt-bh*0.16:.0f}" width="{bw*0.24:.0f}" height="{bh*0.18:.0f}"
      rx="{bw*0.03:.0f}" fill="url(#dg)"/>
<rect x="{bx:.0f}" y="{bt:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{bw*0.10:.0f}" fill="url(#dg)"/>
<rect x="{bx+bw-8:.0f}" y="{bt+bh*0.06:.0f}" width="4" height="{bh*0.84:.0f}" rx="2"
      fill="#FFFFFF" opacity=".7" filter="url(#p1)"/>
{_plate(cx, bt+bh*0.55, bw*0.72, bh*0.30, ('BODY','OIL'))}
{_foot(seed)}'''


# ── a candle in a glass ───────────────────────────────────────────────
def candle(seed=3):
    gw, gh = W*0.40, H*0.40
    gx, gt = (W-gw)/2, BASE-gh
    cx = W/2
    return f'''{_head(seed)}
{_shadow(cx, gw, 0.13)}
<defs>
  <linearGradient id="jar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6E5A44"/><stop offset=".07" stop-color="#D8CCBA"/>
    <stop offset=".2" stop-color="#8A7A66"/><stop offset=".5" stop-color="#C4B6A2"/>
    <stop offset=".76" stop-color="#9A8A74"/><stop offset=".91" stop-color="#F6F0E4"/>
    <stop offset="1" stop-color="#6E5A44"/>
  </linearGradient>
  <linearGradient id="wax2" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#C6B292"/><stop offset=".5" stop-color="#EDE0C8"/>
    <stop offset="1" stop-color="#BFA98A"/>
  </linearGradient>
</defs>
<rect x="{gx:.0f}" y="{gt+gh*0.16:.0f}" width="{gw:.0f}" height="{gh*0.84:.0f}"
      rx="{gw*0.05:.0f}" fill="url(#wax2)"/>
<ellipse cx="{cx:.0f}" cy="{gt+gh*0.17:.0f}" rx="{gw*0.5:.0f}" ry="{gw*0.10:.0f}" fill="#E4D6BC"/>
<ellipse cx="{cx:.0f}" cy="{gt+gh*0.175:.0f}" rx="{gw*0.42:.0f}" ry="{gw*0.075:.0f}" fill="#D4C3A4"/>
<rect x="{cx-2:.0f}" y="{gt+gh*0.10:.0f}" width="4" height="{gh*0.08:.0f}" fill="#4A3A26"/>
<rect x="{gx:.0f}" y="{gt:.0f}" width="{gw:.0f}" height="{gh:.0f}" rx="{gw*0.05:.0f}"
      fill="url(#jar)" opacity=".32"/>
<ellipse cx="{cx:.0f}" cy="{gt:.0f}" rx="{gw*0.5:.0f}" ry="{gw*0.10:.0f}"
         fill="none" stroke="#8A7A66" stroke-width="3" opacity=".7"/>
<path d="M{cx-gw*0.22:.0f} {gt-gw*0.075:.0f} A {gw*0.5:.0f} {gw*0.10:.0f} 0 0 1 {cx+gw*0.46:.0f} {gt-gw*0.02:.0f}"
      stroke="#FFFFFF" stroke-width="5" fill="none" opacity=".85" filter="url(#p1)"/>
<rect x="{gx+gw-9:.0f}" y="{gt+gh*0.10:.0f}" width="4" height="{gh*0.78:.0f}" rx="2"
      fill="#FFFFFF" opacity=".68" filter="url(#p1)"/>
{_plate(cx, gt+gh*0.60, gw*0.50, gh*0.34, ('LA MAISON','DE STEFANIE'))}
{_foot(seed)}'''


# ── a reed diffuser ───────────────────────────────────────────────────
def diffuser(seed=4):
    rnd = random.Random(9)
    bw, bh = W*0.28, H*0.36
    bx, bt = (W-bw)/2, BASE-bh
    cx = W/2
    reeds = ''.join(
        f'<g transform="translate({cx:.0f},{bt+8:.0f}) rotate({-26+i*10.5:.1f})">'
        f'<rect x="-4" y="-{rnd.uniform(300,400):.0f}" width="8" height="{rnd.uniform(300,400):.0f}" '
        f'rx="4" fill="#B8A489"/>'
        f'<rect x="-4" y="-{rnd.uniform(300,400):.0f}" width="3" height="{rnd.uniform(300,400):.0f}" '
        f'rx="1.5" fill="#6E5E48" opacity=".45"/></g>' for i in range(6))
    return f'''{_head(seed)}
{_shadow(cx, bw)}
<defs>
  <linearGradient id="dif" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#3A2A10"/><stop offset=".08" stop-color="#B8933F"/>
    <stop offset=".22" stop-color="#4A3616"/><stop offset=".5" stop-color="#8A6C2E"/>
    <stop offset=".74" stop-color="#C6A45C"/><stop offset=".9" stop-color="#F0DCA8"/>
    <stop offset="1" stop-color="#3A2A10"/>
  </linearGradient>
</defs>
{reeds}
<rect x="{bx:.0f}" y="{bt:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{bw*0.12:.0f}" fill="url(#dif)"/>
<rect x="{cx-bw*0.18:.0f}" y="{bt-bh*0.10:.0f}" width="{bw*0.36:.0f}" height="{bh*0.12:.0f}"
      rx="{bw*0.04:.0f}" fill="url(#dif)"/>
<rect x="{bx+bw-8:.0f}" y="{bt+bh*0.10:.0f}" width="4" height="{bh*0.74:.0f}" rx="2"
      fill="#FFFFFF" opacity=".7" filter="url(#p1)"/>
{_plate(cx, bt+bh*0.56, bw*0.62, bh*0.36, ('REED',))}
{_foot(seed)}'''


# ── a bar of soap ─────────────────────────────────────────────────────
def soap(seed=5):
    bw, bh = W*0.46, H*0.20
    bx, bt = (W-bw)/2, BASE-bh
    cx = W/2
    return f'''{_head(seed)}
{_shadow(cx, bw*0.7, 0.12)}
<defs>
  <linearGradient id="sp" x1=".1" y1="0" x2=".9" y2="1">
    <stop offset="0"   stop-color="#F0E4CE"/>
    <stop offset=".45" stop-color="#DCCBAE"/>
    <stop offset="1"   stop-color="#B8A183"/>
  </linearGradient>
</defs>
<path d="M{bx:.0f} {bt+bh*0.28:.0f} Q {bx:.0f} {bt:.0f} {bx+bw*0.14:.0f} {bt:.0f}
         L{bx+bw*0.86:.0f} {bt:.0f} Q {bx+bw:.0f} {bt:.0f} {bx+bw:.0f} {bt+bh*0.28:.0f}
         L{bx+bw:.0f} {bt+bh*0.72:.0f} Q {bx+bw:.0f} {bt+bh:.0f} {bx+bw*0.86:.0f} {bt+bh:.0f}
         L{bx+bw*0.14:.0f} {bt+bh:.0f} Q {bx:.0f} {bt+bh:.0f} {bx:.0f} {bt+bh*0.72:.0f} Z"
      fill="url(#sp)"/>
<path d="M{bx+bw*0.06:.0f} {bt+8:.0f} L{bx+bw*0.94:.0f} {bt+8:.0f}"
      stroke="#FFFFFF" stroke-width="7" opacity=".65" filter="url(#p4)"/>
<circle cx="{cx:.0f}" cy="{bt+bh*0.5:.0f}" r="{bh*0.30:.0f}" fill="none" stroke="#9C8A6A" stroke-width="2" opacity=".7"/>
<text x="{cx:.0f}" y="{bt+bh*0.5+bh*0.11:.0f}" font-family="Liberation Serif, Georgia, serif"
      font-size="{bh*0.30:.0f}" text-anchor="middle" fill="#9C8A6A" opacity=".85">LS</text>
{_foot(seed)}'''


# ── the voucher / card ────────────────────────────────────────────────
def voucher(seed=6, lines=('THE BESPOKE','SESSION')):
    cw, ch = W*0.56, H*0.36
    cx, cy = W/2, BASE-ch*0.6
    return f'''{_head(seed)}
<ellipse cx="{cx+30:.0f}" cy="{cy+ch*0.56:.0f}" rx="{cw*0.52:.0f}" ry="{cw*0.09:.0f}" fill="url(#cast)"/>
<g transform="rotate(-4 {cx:.0f} {cy:.0f})">
  <rect x="{cx-cw/2:.0f}" y="{cy-ch/2:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="3" fill="#F4EEE0"/>
  <rect x="{cx-cw/2:.0f}" y="{cy-ch/2:.0f}" width="{cw:.0f}" height="{ch:.0f}" rx="3"
        fill="none" stroke="#B99358" stroke-width="1.6" opacity=".8"/>
  <rect x="{cx-cw/2+16:.0f}" y="{cy-ch/2+16:.0f}" width="{cw-32:.0f}" height="{ch-32:.0f}"
        fill="none" stroke="#B99358" stroke-width="1" opacity=".45"/>
  <g font-family="Liberation Serif, DejaVu Serif, Georgia, serif" text-anchor="middle" fill="#43341F">
    {''.join(f'<text x="{cx:.0f}" y="{cy-ch*0.10+i*40:.0f}" font-size="30" letter-spacing="3">{t}</text>' for i,t in enumerate(lines))}
    <text x="{cx:.0f}" y="{cy+ch*0.30:.0f}" font-size="14" letter-spacing="6" fill="#7A6544">LA MAISON DE STEFANIE</text>
  </g>
  <rect x="{cx-cw/2:.0f}" y="{cy-ch/2:.0f}" width="{cw*0.34:.0f}" height="{ch:.0f}" fill="#8A7A62" opacity=".08"/>
</g>
{_foot(seed)}'''
