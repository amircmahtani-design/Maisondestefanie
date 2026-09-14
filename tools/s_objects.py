# -*- coding: utf-8 -*-
"""The two other things on the counter: the blending bowl and the rose.
Both come out on transparency so they can be layered into the hero."""
import math, random

COMMON_FILTERS = '''
  <filter id="s2"  x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="s5"  x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="5"/></filter>
  <filter id="s9"  x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="9"/></filter>
  <filter id="s12" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="s28" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="28"/></filter>
  <filter id="s60" x="-95%" y="-95%" width="290%" height="290%"><feGaussianBlur stdDeviation="60"/></filter>
'''

GRAIN = '''
  <filter id="grn"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="4"/></filter>
'''


def grain(w, h, o='.05'):
    return (f'<g style="mix-blend-mode:overlay" opacity="{o}">'
            f'<rect width="{w}" height="{h}" filter="url(#grn)"/></g>')


# ══════════════════════════════════════════════════════════════════════
# THE BLENDING BOWL
#   A shallow glass bowl of oil. Almost all of it is dark; the bowl is
#   described by three or four highlights and the pool of light it
#   throws forward onto the counter.
# ══════════════════════════════════════════════════════════════════════
def vessel(W=1200, H=900):
    cx = W / 2
    rim_y, rim_rx, rim_ry = 352, 296, 62      # the mouth
    depth = 268                               # how far down the bowl goes
    base_y = rim_y + depth
    oil_y = 424
    oil_rx, oil_ry = 268, 54

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{COMMON_FILTERS}{GRAIN}
  <!-- the oil, seen through the side of the bowl: black at the edges
       where you look through most of it, alight where the key gets in -->
  <radialGradient id="oilBody" cx=".63" cy=".18" r=".92">
    <stop offset="0"   stop-color="#D9913C"/>
    <stop offset=".20" stop-color="#A0601D"/>
    <stop offset=".44" stop-color="#5E320C"/>
    <stop offset=".72" stop-color="#2A1304"/>
    <stop offset="1"   stop-color="#100701"/>
  </radialGradient>
  <radialGradient id="oilFace" cx=".62" cy=".30" r=".78">
    <stop offset="0"   stop-color="#F6C87E"/>
    <stop offset=".22" stop-color="#C4832C"/>
    <stop offset=".55" stop-color="#6E3C0E"/>
    <stop offset=".84" stop-color="#331A04"/>
    <stop offset="1"   stop-color="#1A0C02"/>
  </radialGradient>
  <radialGradient id="pool" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#FFCE8A" stop-opacity=".72"/>
    <stop offset=".36" stop-color="#B8701F" stop-opacity=".30"/>
    <stop offset="1"   stop-color="#7A4410" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="shade" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#000000" stop-opacity=".92"/>
    <stop offset=".55" stop-color="#000000" stop-opacity=".38"/>
    <stop offset="1"   stop-color="#000000" stop-opacity="0"/>
  </radialGradient>

  <!-- the silhouette of the glass, used to keep every highlight on it -->
  <clipPath id="bowl">
    <path d="M{cx-rim_rx} {rim_y}
             C {cx-rim_rx} {rim_y+depth*0.86} {cx-rim_rx*0.52} {base_y} {cx} {base_y}
             C {cx+rim_rx*0.52} {base_y} {cx+rim_rx} {rim_y+depth*0.86} {cx+rim_rx} {rim_y}
             A {rim_rx} {rim_ry} 0 0 1 {cx-rim_rx} {rim_y} Z"/>
  </clipPath>
</defs>

<!-- the air around it -->
<ellipse cx="{cx+30}" cy="470" rx="400" ry="270" fill="#B8761F" opacity=".13"
         filter="url(#s60)" style="mix-blend-mode:screen"/>

<!-- it sits on the counter -->
<ellipse cx="{cx}" cy="{base_y-6}" rx="240" ry="34" fill="url(#shade)"/>
<ellipse cx="{cx+56}" cy="{base_y+2}" rx="196" ry="26" fill="url(#pool)" style="mix-blend-mode:screen"/>

<g clip-path="url(#bowl)">
  <!-- everything below the oil line is the oil, seen through glass -->
  <rect x="0" y="{oil_y}" width="{W}" height="{H}" fill="url(#oilBody)"/>
  <!-- above it, the empty glass is almost nothing -->
  <rect x="0" y="0" width="{W}" height="{oil_y}" fill="#1A1108" opacity=".28"/>
  <!-- the key light coming through the body of the oil -->
  <ellipse cx="{cx+92}" cy="{oil_y+96}" rx="128" ry="96" fill="#FFCE8A"
           opacity=".28" filter="url(#s28)"/>
  <!-- and dying out to the left -->
  <ellipse cx="{cx-210}" cy="{oil_y+120}" rx="180" ry="180" fill="#000000"
           opacity=".55" filter="url(#s28)"/>
</g>

<!-- the surface of the oil -->
<ellipse cx="{cx}" cy="{oil_y}" rx="{oil_rx}" ry="{oil_ry}" fill="url(#oilFace)"/>
<ellipse cx="{cx}" cy="{oil_y}" rx="{oil_rx}" ry="{oil_ry}" fill="none"
         stroke="#E8B87A" stroke-width="1.6" opacity=".4"/>
<!-- what the room puts back on it -->
<ellipse cx="{cx+74}" cy="{oil_y-16}" rx="84" ry="15" fill="#FFEBC4" opacity=".5" filter="url(#s9)"/>
<ellipse cx="{cx-104}" cy="{oil_y+6}" rx="38" ry="7"  fill="#E8C48A" opacity=".16" filter="url(#s9)"/>

<!-- a petal, floating, mostly in shadow -->
<g transform="translate({cx+104},{oil_y+14}) rotate(-14)">
  <ellipse cx="0" cy="0" rx="50" ry="24" fill="#42101B"/>
  <ellipse cx="-8" cy="-3" rx="40" ry="18" fill="#611B29"/>
  <ellipse cx="-16" cy="-6" rx="24" ry="10" fill="#8A3244" opacity=".65"/>
  <ellipse cx="6" cy="8" rx="40" ry="10" fill="#1E0710" opacity=".7"/>
</g>

<!-- ══ the glass itself: three highlights and nothing else ══ -->
<!-- the rim, from behind and in front -->
<ellipse cx="{cx}" cy="{rim_y}" rx="{rim_rx}" ry="{rim_ry}" fill="none"
         stroke="#6E5A38" stroke-width="2.4" opacity=".5"/>
<path d="M{cx-46} {rim_y-rim_ry+2} A {rim_rx} {rim_ry} 0 0 1 {cx+rim_rx-10} {rim_y-18}"
      stroke="#FFFDF6" stroke-width="6" fill="none" opacity=".92" filter="url(#s2)"/>
<path d="M{cx-rim_rx+8} {rim_y-12} A {rim_rx} {rim_ry} 0 0 1 {cx-130} {rim_y-rim_ry+6}"
      stroke="#F2DCB0" stroke-width="3.4" fill="none" opacity=".34" filter="url(#s2)"/>
<!-- the lit side wall, following the real silhouette -->
<path d="M{cx+rim_rx-6} {rim_y+16}
         C {cx+rim_rx-8} {rim_y+depth*0.72} {cx+rim_rx*0.62} {base_y-14} {cx+96} {base_y-8}"
      stroke="#FFF2D8" stroke-width="7" fill="none" opacity=".55" filter="url(#s5)"
      stroke-linecap="round"/>
<path d="M{cx-rim_rx+6} {rim_y+22}
         C {cx-rim_rx+8} {rim_y+depth*0.68} {cx-rim_rx*0.66} {base_y-18} {cx-116} {base_y-12}"
      stroke="#D8B078" stroke-width="4" fill="none" opacity=".2" filter="url(#s5)"
      stroke-linecap="round"/>
<!-- the thick foot -->
<ellipse cx="{cx}" cy="{base_y-12}" rx="104" ry="18" fill="#FFD79A" opacity=".34" filter="url(#s9)"/>

{grain(W,H)}
</svg>'''


# ══════════════════════════════════════════════════════════════════════
# THE ROSE
#   Opaque petals, each sitting in its own shadow, almost all of it in
#   deep burgundy. Only the petals turned towards the key get any light.
# ══════════════════════════════════════════════════════════════════════
def rose(W=1200, H=900, seed=31):
    rnd = random.Random(seed)
    cx, cy = W * 0.47, H * 0.53
    KEY = math.radians(-40)                   # the light, upper right

    #  spread  size  n  phase  base       lit
    rings = [
        (2.00, 258, 9, 0.00, '#230510', '#5E1524'),
        (1.66, 214, 8, 0.34, '#2A0713', '#6E1B2A'),
        (1.32, 176, 8, 0.14, '#320A17', '#7C2232'),
        (1.02, 142, 7, 0.52, '#3A0D1B', '#88283A'),
        (0.76, 112, 6, 0.26, '#420F1F', '#8E2E40'),
        (0.54,  86, 5, 0.66, '#3A0C1A', '#762436'),
        (0.34,  62, 4, 0.08, '#2E0814', '#4A1220'),
        (0.18,  42, 3, 0.44, '#240611', '#5E1A28'),
    ]

    out = []
    pid = 0
    for spread, pr, n, phase, base, lit in rings:
        for k in range(n):
            a = (k / n + phase) * 2 * math.pi + rnd.uniform(-0.10, 0.10)
            rad = pr * spread * 0.46
            px = cx + math.cos(a) * rad * 1.06
            py = cy + math.sin(a) * rad * 0.80
            w = pr * rnd.uniform(0.80, 1.06)
            h = pr * rnd.uniform(0.86, 1.16)
            rot = math.degrees(a) + 90 + rnd.uniform(-14, 14)
            face = max(0.0, math.cos(a - KEY)) ** 1.5
            pid += 1
            gid = f'pg{pid}'
            # a cupped petal: broad, softly notched at the tip, narrow at the base
            d = (f'M0 {h*0.98:.0f} '
                 f'C {-w*0.86:.0f} {h*0.52:.0f} {-w*1.0:.0f} {-h*0.44:.0f} {-w*0.30:.0f} {-h*0.92:.0f} '
                 f'C {-w*0.10:.0f} {-h*1.02:.0f} {w*0.10:.0f} {-h*1.02:.0f} {w*0.30:.0f} {-h*0.92:.0f} '
                 f'C {w*1.0:.0f} {-h*0.44:.0f} {w*0.86:.0f} {h*0.52:.0f} 0 {h*0.98:.0f} Z')
            out.append(f'''
  <g transform="translate({px:.1f},{py:.1f}) rotate({rot:.1f})">
    <defs>
      <linearGradient id="{gid}" x1=".5" y1="1" x2=".42" y2="0">
        <stop offset="0"   stop-color="#150309"/>
        <stop offset=".26" stop-color="{base}"/>
        <stop offset=".72" stop-color="{_mix(base, lit, 0.25 + face*0.55)}"/>
        <stop offset="1"   stop-color="{_mix(base, lit, 0.40 + face*0.60)}"/>
      </linearGradient>
    </defs>
    <path d="{d}" fill="#0B0206" opacity=".85" filter="url(#drop)"
          transform="translate(2,{h*0.10:.0f}) scale(1.06)"/>
    <path d="{d}" fill="url(#{gid})" filter="url(#curl)"/>
    <path d="M{-w*0.24:.0f} {-h*0.88:.0f} C {-w*0.10:.0f} {-h*0.98:.0f} {w*0.10:.0f} {-h*0.98:.0f} {w*0.24:.0f} {-h*0.88:.0f}"
          stroke="{lit}" stroke-width="{max(1.2, w*0.05):.1f}" fill="none"
          opacity="{0.12 + face*0.62:.2f}" filter="url(#s2)"/>
  </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{COMMON_FILTERS}{GRAIN}
  <filter id="curl" x="-40%" y="-40%" width="180%" height="180%">
    <feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="3" seed="21" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="17" xChannelSelector="R" yChannelSelector="G"/>
    <feGaussianBlur stdDeviation=".8"/>
  </filter>
  <filter id="drop" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="leafCurl" x="-40%" y="-40%" width="180%" height="180%">
    <feTurbulence type="fractalNoise" baseFrequency=".016" numOctaves="3" seed="6" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="20" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <radialGradient id="rShade" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#000000" stop-opacity=".85"/>
    <stop offset=".6"  stop-color="#000000" stop-opacity=".28"/>
    <stop offset="1"   stop-color="#000000" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="leaf" x1=".2" y1="0" x2="1" y2="1">
    <stop offset="0"   stop-color="#24301A"/>
    <stop offset=".45" stop-color="#141B0F"/>
    <stop offset="1"   stop-color="#080B06"/>
  </linearGradient>
</defs>

<ellipse cx="{cx+90}" cy="{cy-70}" rx="300" ry="240" fill="#7E1E30" opacity=".17"
         filter="url(#s60)" style="mix-blend-mode:screen"/>

<ellipse cx="{cx+10}" cy="{cy+206}" rx="330" ry="62" fill="url(#rShade)"/>

<g filter="url(#leafCurl)" opacity=".95">
  <path d="M{cx-336} {cy+140} C {cx-450} {cy+50} {cx-410} {cy-80} {cx-248} {cy-46}
           C {cx-262} {cy+64} {cx-250} {cy+124} {cx-336} {cy+140} Z" fill="url(#leaf)"/>
  <path d="M{cx+262} {cy+196} C {cx+404} {cy+164} {cx+430} {cy+44} {cx+306} {cy+34}
           C {cx+306} {cy+118} {cx+318} {cy+162} {cx+262} {cy+196} Z" fill="url(#leaf)"/>
</g>

{''.join(out)}

<!-- the key grazes the upper right of the bloom -->
<ellipse cx="{cx+150}" cy="{cy-140}" rx="150" ry="112" fill="#C4405A" opacity=".13"
         filter="url(#s28)" style="mix-blend-mode:screen"/>
<!-- everything else goes to nothing -->
<ellipse cx="{cx-270}" cy="{cy+60}" rx="270" ry="250" fill="#040104" opacity=".42" filter="url(#s60)"/>
<ellipse cx="{cx-40}" cy="{cy+300}" rx="400" ry="150" fill="#040104" opacity=".36" filter="url(#s60)"/>

{grain(W,H,'.06')}
</svg>'''


def _mix(a, b, t):
    """Blend two hex colours, so a petal's lit end is genuinely its own
       colour lifted rather than a different hue pasted on."""
    t = max(0.0, min(1.0, t))
    ai = [int(a[1:][i:i+2], 16) for i in (0, 2, 4)]
    bi = [int(b[1:][i:i+2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(ai, bi))
