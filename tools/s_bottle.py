# -*- coding: utf-8 -*-
"""The flacon — a slab of amber glass with a gold ball stopper, lit from
the right, standing on a dark polished counter."""

W, H = 900, 1200
BX, BW = 258, 384                 # body left edge / width
BT, BB = 452, 1044                # body top / bottom
CX     = BX + BW / 2              # 450
BR     = BX + BW                  # 642
NW     = 92                       # neck width
NT     = 352                      # neck top
CAP_CY = 248
CAP_R  = 72


def build():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <!-- Amber glass seen side-on and lit from the right: the edges read
       dark because you are looking through more glass, the core glows,
       and a hot specular sits just inside the right edge. -->
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#2A1404"/>
    <stop offset=".045" stop-color="#93531A"/>
    <stop offset=".105" stop-color="#4B2408"/>
    <stop offset=".30"  stop-color="#9A5A1E"/>
    <stop offset=".50"  stop-color="#B96F26"/>
    <stop offset=".655" stop-color="#7A4212"/>
    <stop offset=".80"  stop-color="#D9964A"/>
    <stop offset=".895" stop-color="#FAE0B0"/>
    <stop offset=".955" stop-color="#C07E30"/>
    <stop offset="1"    stop-color="#3D1D05"/>
  </linearGradient>

  <!-- the liquid is denser at the bottom and the shoulder falls to shadow -->
  <linearGradient id="depth" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="#000000" stop-opacity=".62"/>
    <stop offset=".14"  stop-color="#000000" stop-opacity=".18"/>
    <stop offset=".55"  stop-color="#000000" stop-opacity="0"/>
    <stop offset=".88"  stop-color="#2A1002" stop-opacity=".34"/>
    <stop offset="1"    stop-color="#170800" stop-opacity=".62"/>
  </linearGradient>

  <linearGradient id="neckGlass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#2A1404"/>
    <stop offset=".18"  stop-color="#7C4413"/>
    <stop offset=".46"  stop-color="#A96227"/>
    <stop offset=".72"  stop-color="#6B3810"/>
    <stop offset=".88"  stop-color="#F5CE92"/>
    <stop offset="1"    stop-color="#341903"/>
  </linearGradient>

  <!-- gold, turned: a bright crescent where the light lands, a dark
       belly, and a thin bounce coming back up from the counter -->
  <radialGradient id="gold" cx=".64" cy=".30" r=".92">
    <stop offset="0"   stop-color="#FBEBC6"/>
    <stop offset=".16" stop-color="#E4C489"/>
    <stop offset=".38" stop-color="#B08A48"/>
    <stop offset=".62" stop-color="#6E5123"/>
    <stop offset=".78" stop-color="#4A3416"/>
    <stop offset=".93" stop-color="#8A6A32"/>
    <stop offset="1"   stop-color="#2E2109"/>
  </radialGradient>

  <linearGradient id="collar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#3B2C11"/>
    <stop offset=".16"  stop-color="#8A6C32"/>
    <stop offset=".40"  stop-color="#5E4720"/>
    <stop offset=".70"  stop-color="#C6A45C"/>
    <stop offset=".86"  stop-color="#F0DCAC"/>
    <stop offset="1"    stop-color="#4A3616"/>
  </linearGradient>

  <linearGradient id="plateShade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"   stop-color="#2E1B05" stop-opacity=".34"/>
    <stop offset=".42" stop-color="#2E1B05" stop-opacity=".10"/>
    <stop offset=".78" stop-color="#2E1B05" stop-opacity="0"/>
    <stop offset="1"   stop-color="#FFE7BC" stop-opacity=".22"/>
  </linearGradient>
  <linearGradient id="plate" x1=".1" y1="0" x2="1" y2=".6">
    <stop offset="0"   stop-color="#D8CCB4"/>
    <stop offset=".45" stop-color="#EFE6D2"/>
    <stop offset="1"   stop-color="#C9BB9E"/>
  </linearGradient>

  <radialGradient id="halo" cx=".5" cy=".55" r=".5">
    <stop offset="0"   stop-color="#C98A3A" stop-opacity=".52"/>
    <stop offset=".55" stop-color="#8A4E14" stop-opacity=".18"/>
    <stop offset="1"   stop-color="#8A4E14" stop-opacity="0"/>
  </radialGradient>

  <radialGradient id="caustic" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#FFD08A" stop-opacity=".85"/>
    <stop offset=".38" stop-color="#C97F26" stop-opacity=".38"/>
    <stop offset="1"   stop-color="#8A4E14" stop-opacity="0"/>
  </radialGradient>

  <radialGradient id="contact" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#000000" stop-opacity=".92"/>
    <stop offset=".55" stop-color="#000000" stop-opacity=".45"/>
    <stop offset="1"   stop-color="#000000" stop-opacity="0"/>
  </radialGradient>

  <filter id="soft8"  x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="soft3"  x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="soft18" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="soft40" x="-90%" y="-90%" width="280%" height="280%"><feGaussianBlur stdDeviation="40"/></filter>

  <!-- the faint irregularity of hand-poured glass -->
  <filter id="glassGrain" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".006 .09" numOctaves="3" seed="9" result="t"/>
    <feDisplacementMap in="SourceGraphic" in2="t" scale="7" xChannelSelector="R" yChannelSelector="G"/>
  </filter>

  <clipPath id="bodyClip">
    <rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30"/>
  </clipPath>

  <linearGradient id="reflFade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="#ffffff" stop-opacity=".30"/>
    <stop offset=".55" stop-color="#ffffff" stop-opacity=".05"/>
    <stop offset="1"   stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <mask id="reflMask">
    <rect x="0" y="{BB}" width="{W}" height="240" fill="url(#reflFade)"/>
  </mask>
</defs>

<!-- ── the air around it warms up ── -->
<ellipse cx="{CX}" cy="700" rx="330" ry="420" fill="url(#halo)" style="mix-blend-mode:screen"/>

<!-- ── it stands on something ── -->
<ellipse cx="{CX}" cy="{BB+16}" rx="250" ry="44" fill="url(#contact)"/>
<ellipse cx="{CX+26}" cy="{BB+10}" rx="170" ry="26" fill="url(#caustic)" style="mix-blend-mode:screen"/>

<!-- ── the reflection in the counter ── -->
<g mask="url(#reflMask)" opacity=".55">
  <g transform="translate(0,{2*BB}) scale(1,-1)">
    <rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30" fill="url(#glass)"/>
    <rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30" fill="url(#depth)"/>
  </g>
</g>

<!-- ══ THE NECK, behind the collar ══ -->
<rect x="{CX-NW/2}" y="{NT}" width="{NW}" height="{BT-NT+40}" rx="10" fill="#5C3110"/>
<rect x="{CX-NW/2}" y="{NT}" width="{NW}" height="{BT-NT+40}" rx="10" fill="url(#neckGlass)" opacity=".9"/>
<rect x="{CX+NW/2-9}" y="{NT+4}" width="4" height="{BT-NT+28}" rx="2" fill="#FBE7BE" opacity=".55" filter="url(#soft3)"/>

<!-- ══ THE BODY ══ -->
<g filter="url(#glassGrain)">
  <rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30" fill="url(#glass)"/>
</g>
<rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30" fill="url(#depth)"/>

<g clip-path="url(#bodyClip)">
  <!-- light travelling down through the liquid -->
  <rect x="{BX+52}" y="{BT}" width="26" height="{BB-BT}" fill="#F6D8A4" opacity=".14" filter="url(#soft18)"/>
  <rect x="{BX+236}" y="{BT}" width="52" height="{BB-BT}" fill="#FFE2B4" opacity=".2" filter="url(#soft18)"/>
  <!-- the shoulder catches the key light -->
  <ellipse cx="{CX+70}" cy="{BT+30}" rx="150" ry="34" fill="#FFE6BE" opacity=".38" filter="url(#soft18)"/>
  <!-- and the base pools it -->
  <ellipse cx="{CX+20}" cy="{BB-24}" rx="180" ry="40" fill="#FFC97E" opacity=".3" filter="url(#soft18)"/>
  <!-- the surface of the liquid -->
  <path d="M{BX} {BT+96} Q {CX} {BT+112} {BR} {BT+92}" stroke="#FFDCA6" stroke-width="3"
        fill="none" opacity=".5" filter="url(#soft3)"/>
  <rect x="{BX}" y="{BT}" width="{BW}" height="96" fill="#1B0C02" opacity=".5"/>
  <!-- the foot, where the glass thickens -->
  <rect x="{BX}" y="{BB-46}" width="{BW}" height="46" fill="#251002" opacity=".45"/>
  <ellipse cx="{CX+30}" cy="{BB-40}" rx="120" ry="12" fill="#FFDDA4" opacity=".5" filter="url(#soft8)"/>
</g>

<!-- the edges: thin, bright, and only where the light can reach -->
<rect x="{BX}" y="{BT}" width="{BW}" height="{BB-BT}" rx="30" fill="none"
      stroke="#7A4A18" stroke-width="2" opacity=".8"/>
<path d="M{BR-4} {BT+34} L{BR-4} {BB-52}" stroke="#FFF0D2" stroke-width="7"
      stroke-linecap="round" fill="none" opacity=".82" filter="url(#soft3)"/>
<path d="M{BR-7} {BT+90} L{BR-7} {BB-140}" stroke="#FFFBF0" stroke-width="2.5"
      stroke-linecap="round" fill="none" opacity=".9"/>
<path d="M{BX+5} {BT+58} L{BX+5} {BB-90}" stroke="#F0BE78" stroke-width="4"
      stroke-linecap="round" fill="none" opacity=".38" filter="url(#soft3)"/>
<path d="M{BX+36} {BT+3} Q {CX+40} {BT-6} {BR-34} {BT+7}" stroke="#FFEBCB" stroke-width="5"
      stroke-linecap="round" fill="none" opacity=".6" filter="url(#soft3)"/>

<!-- ══ THE LABEL PLATE ══ -->
<g>
  <rect x="{CX-124}" y="668" width="248" height="196" rx="3" fill="#2A1503" opacity=".5" filter="url(#soft8)"/>
  <rect x="{CX-120}" y="664" width="240" height="188" rx="2" fill="url(#plate)"/>
  <rect x="{CX-120}" y="664" width="240" height="188" rx="2" fill="none" stroke="#9C8253" stroke-width="1.2" opacity=".7"/>
  <rect x="{CX-108}" y="676" width="216" height="164" rx="1" fill="none" stroke="#A08A5E" stroke-width=".8" opacity=".5"/>
  <g font-family="Liberation Serif, DejaVu Serif, Georgia, serif" text-anchor="middle" fill="#3B2E1C">
    <text x="{CX}" y="736" font-size="25" letter-spacing="2.6">LA MAISON</text>
    <text x="{CX}" y="770" font-size="25" letter-spacing="2.6">DE STEFANIE</text>
    <text x="{CX}" y="806" font-size="17" fill="#7A6438">&#8212;</text>
    <text x="{CX}" y="832" font-size="13" letter-spacing="5.5" fill="#6B573A">ATHENS</text>
  </g>
  <!-- the paper takes the same light as everything else -->
  <rect x="{CX-120}" y="664" width="240" height="188" rx="2" fill="url(#plateShade)"/>
</g>

<!-- ══ THE COLLAR ══ -->
<rect x="{CX-58}" y="330" width="116" height="34" rx="6" fill="url(#collar)"/>
<rect x="{CX-58}" y="330" width="116" height="34" rx="6" fill="none" stroke="#33260D" stroke-width="1.2"/>
<rect x="{CX-52}" y="336" width="104" height="4" rx="2" fill="#FFF2CE" opacity=".5" filter="url(#soft3)"/>

<!-- ══ THE STOPPER ══ -->
<ellipse cx="{CX}" cy="{CAP_CY+CAP_R-8}" rx="{CAP_R*0.8}" ry="14" fill="#1A1205" opacity=".8" filter="url(#soft8)"/>
<circle cx="{CX}" cy="{CAP_CY}" r="{CAP_R}" fill="url(#gold)"/>
<circle cx="{CX}" cy="{CAP_CY}" r="{CAP_R}" fill="none" stroke="#F4E0AE" stroke-width="2" opacity=".28"/>
<!-- the key light, small and hard -->
<ellipse cx="{CX+26}" cy="{CAP_CY-32}" rx="19" ry="13" fill="#FFF8E4" opacity=".95"
         transform="rotate(-24 {CX+26} {CAP_CY-32})" filter="url(#soft3)"/>
<ellipse cx="{CX+38}" cy="{CAP_CY-16}" rx="7" ry="5" fill="#FFFFFF" opacity=".8"/>
<!-- the counter throwing a little back up -->
<path d="M{CX-52} {CAP_CY+44} A {CAP_R} {CAP_R} 0 0 0 {CX+50} {CAP_CY+46}"
      stroke="#D9B36A" stroke-width="7" fill="none" opacity=".45" filter="url(#soft3)"/>

{_grain()}
</svg>'''


def _grain():
    return f'''<g style="mix-blend-mode:overlay" opacity=".05">
  <filter id="gn"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="5"/></filter>
  <rect width="{W}" height="{H}" filter="url(#gn)"/>
</g>'''


if __name__ == '__main__':
    import sys
    open(sys.argv[1] if len(sys.argv) > 1 else 'scenes/bottle.svg', 'w',
         encoding='utf-8').write(build())
    print('bottle.svg written')
