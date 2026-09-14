# -*- coding: utf-8 -*-
"""Shared parts. One warm source from the upper right, deep falloff
everywhere else, and everything shaded rather than filled flat."""
import math, random

FILTERS = '''
  <filter id="b1"   x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="1"/></filter>
  <filter id="b2"   x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="b4"   x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="b8"   x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="b16"  x="-85%" y="-85%" width="270%" height="270%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="b30"  x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="30"/></filter>
  <filter id="b60"  x="-95%" y="-95%" width="290%" height="290%"><feGaussianBlur stdDeviation="60"/></filter>
  <filter id="b120" x="-99%" y="-99%" width="300%" height="300%"><feGaussianBlur stdDeviation="120"/></filter>
  <filter id="b240" x="-99%" y="-99%" width="300%" height="300%"><feGaussianBlur stdDeviation="240"/></filter>
'''

_tex_n = [0]


def texture(w, h, freq='.004 .011', oct_=5, seed=3, op='.42', mode='overlay'):
    """Tonal variation laid *over* what is already there, so it modulates
       the colour instead of replacing it with grey."""
    _tex_n[0] += 1
    i = f'tx{_tex_n[0]}_{seed}'
    return (f'<filter id="{i}"><feTurbulence type="fractalNoise" baseFrequency="{freq}" '
            f'numOctaves="{oct_}" seed="{seed}"/></filter>'
            f'<g style="mix-blend-mode:{mode}" opacity="{op}">'
            f'<rect width="{w}" height="{h}" filter="url(#{i})"/></g>')


def grain(w, h, o='.05', seed=8):
    _tex_n[0] += 1
    i = f'gn{_tex_n[0]}_{seed}'
    return (f'<filter id="{i}"><feTurbulence type="fractalNoise" baseFrequency=".85" '
            f'numOctaves="3" seed="{seed}"/></filter>'
            f'<g style="mix-blend-mode:overlay" opacity="{o}">'
            f'<rect width="{w}" height="{h}" filter="url(#{i})"/></g>')


def vignette_def(strength='.86'):
    return f'''
  <radialGradient id="vig" cx=".58" cy=".40" r=".78">
    <stop offset=".22" stop-color="#000000" stop-opacity="0"/>
    <stop offset=".58" stop-color="#000000" stop-opacity=".26"/>
    <stop offset=".82" stop-color="#000000" stop-opacity=".60"/>
    <stop offset="1"   stop-color="#000000" stop-opacity="{strength}"/>
  </radialGradient>'''


def bloom(x, y, rx, ry, col='#E8A94F', op='.3', f='b60'):
    return (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" '
            f'opacity="{op}" filter="url(#{f})" style="mix-blend-mode:screen"/>')


def dark(x, y, rx, ry, op='.6', f='b120'):
    return (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" '
            f'fill="#040203" opacity="{op}" filter="url(#{f})"/>')


def head(W, H, extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><defs>{FILTERS}{vignette_def()}{extra}</defs>')


def foot(W, H, gr='.05', seed=8):
    return (f'<rect width="{W}" height="{H}" fill="url(#vig)"/>'
            f'{grain(W,H,gr,seed)}</svg>')


# ── a bottle with real shading, at any size ──────────────────────────
_b_n = [0]


def bottle(x, base, w, h, key=1.0, blur=None, hue='amber', label=False):
    """key: 0..1, how much of the source this one sees.
       blur: an id from FILTERS, for anything off the focal plane."""
    _b_n[0] += 1
    g = f'bg{_b_n[0]}'
    nw, sh = w * 0.30, h * 0.24
    fl = f' filter="url(#{blur})"' if blur else ''
    k = max(0.0, min(1.0, key))
    ramps = {
        'amber':  ('#160A02', '#4A2408', '#8A4E14', '#C88132', '#F3D296'),
        'green':  ('#0A0F07', '#16240F', '#2A3C1A', '#4E6B2E', '#A8C070'),
        'clear':  ('#0C0A07', '#1E1912', '#3A3226', '#6E6048', '#E8DCC0'),
        'smoke':  ('#0A0806', '#181310', '#2C231C', '#4E3E32', '#B8A08A'),
    }
    a, b, c, d, e = ramps.get(hue, ramps['amber'])
    lab = ''
    if label and w > 60:
        lw, lh = w * 0.56, h * 0.24
        lab = (f'<rect x="{x-lw/2:.1f}" y="{base-h*0.56:.1f}" width="{lw:.1f}" height="{lh:.1f}" '
               f'rx="1" fill="#7A6A4A" opacity="{0.30+k*0.42:.2f}"/>'
               f'<rect x="{x-lw/2:.1f}" y="{base-h*0.56:.1f}" width="{lw*0.42:.1f}" height="{lh:.1f}" '
               f'fill="#0A0604" opacity=".3"/>')
    return f'''<g{fl}>
    <defs>
      <linearGradient id="{g}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0"    stop-color="{a}"/>
        <stop offset=".07"  stop-color="{c}" stop-opacity="{0.3+k*0.6:.2f}"/>
        <stop offset=".22"  stop-color="{b}"/>
        <stop offset=".52"  stop-color="{c}"/>
        <stop offset=".70"  stop-color="{b}"/>
        <stop offset=".85"  stop-color="{d}"/>
        <stop offset=".93"  stop-color="{e}"/>
        <stop offset="1"    stop-color="{a}"/>
      </linearGradient>
    </defs>
    <ellipse cx="{x:.0f}" cy="{base+w*0.05:.0f}" rx="{w*0.62:.0f}" ry="{w*0.14:.0f}"
             fill="#000" opacity=".72" filter="url(#b8)"/>
    <path d="M{x-w/2:.1f} {base:.1f} L{x-w/2:.1f} {base-h+sh:.1f}
             C {x-w/2:.1f} {base-h:.1f} {x-nw/2:.1f} {base-h+4:.1f} {x-nw/2:.1f} {base-h-h*0.20:.1f}
             L{x+nw/2:.1f} {base-h-h*0.20:.1f}
             C {x+nw/2:.1f} {base-h+4:.1f} {x+w/2:.1f} {base-h:.1f} {x+w/2:.1f} {base-h+sh:.1f}
             L{x+w/2:.1f} {base:.1f} Z" fill="url(#{g})" opacity="{0.42+k*0.58:.2f}"/>
    <rect x="{x-nw/2-w*0.05:.1f}" y="{base-h-h*0.30:.1f}" width="{nw+w*0.10:.1f}"
          height="{h*0.11:.1f}" rx="{w*0.03:.1f}" fill="{b}" opacity="{0.5+k*0.5:.2f}"/>
    <path d="M{x+w/2-w*0.055:.1f} {base-h*0.10:.1f} L{x+w/2-w*0.055:.1f} {base-h+sh*0.9:.1f}"
          stroke="{e}" stroke-width="{max(1.0,w*0.05):.1f}" opacity="{0.15+k*0.8:.2f}"
          stroke-linecap="round" filter="url(#b1)"/>
    {lab}
  </g>'''


def bokeh(rnd, n, x0, x1, y0, y1, rmin, rmax, col='#D8973C', op=(0.04, 0.18), f='b30'):
    return ''.join(
        f'<circle cx="{rnd.uniform(x0,x1):.0f}" cy="{rnd.uniform(y0,y1):.0f}" '
        f'r="{rnd.uniform(rmin,rmax):.0f}" fill="{col}" opacity="{rnd.uniform(*op):.2f}" '
        f'filter="url(#{f})" style="mix-blend-mode:screen"/>' for _ in range(n))


def petal(x, y, r, rot, key=1.0, seed=0):
    k = max(0.05, min(1.0, key))
    return f'''<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})">
    <ellipse cx="3" cy="5" rx="{r:.0f}" ry="{r*0.55:.0f}" fill="#000" opacity=".6" filter="url(#b8)"/>
    <ellipse cx="0" cy="0" rx="{r:.0f}" ry="{r*0.52:.0f}" fill="#2A0810"/>
    <ellipse cx="{-r*0.10:.0f}" cy="{-r*0.07:.0f}" rx="{r*0.86:.0f}" ry="{r*0.40:.0f}"
             fill="#5E1524" opacity="{0.35+k*0.55:.2f}"/>
    <ellipse cx="{-r*0.22:.0f}" cy="{-r*0.12:.0f}" rx="{r*0.5:.0f}" ry="{r*0.19:.0f}"
             fill="#8E2E40" opacity="{k*0.55:.2f}"/>
    <path d="M{-r*0.8:.0f} {r*0.1:.0f} Q 0 {-r*0.34:.0f} {r*0.8:.0f} {r*0.05:.0f}"
          stroke="#A8394A" stroke-width="{max(1,r*0.05):.1f}" fill="none" opacity="{k*0.3:.2f}"/>
  </g>'''
