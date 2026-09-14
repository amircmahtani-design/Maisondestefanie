# -*- coding: utf-8 -*-
"""Chapter three's subject: a graduated glass with an accord in it and a
pipette above, mid-drop. Cut out on transparency like the others."""

W, H = 1100, 1400
CX = W / 2


def build():
    gx, gw = CX - 190, 380          # glass
    gt, gb = 620, 1290
    liq = 830
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="cglass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#231A10" stop-opacity=".55"/>
    <stop offset=".07"  stop-color="#F2E2C0" stop-opacity=".55"/>
    <stop offset=".18"  stop-color="#4A3A24" stop-opacity=".22"/>
    <stop offset=".52"  stop-color="#8A7048" stop-opacity=".14"/>
    <stop offset=".80"  stop-color="#F6E8CA" stop-opacity=".42"/>
    <stop offset=".92"  stop-color="#FFFBF0" stop-opacity=".78"/>
    <stop offset="1"    stop-color="#3A2C18" stop-opacity=".5"/>
  </linearGradient>
  <linearGradient id="accord" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"    stop-color="#2A1304"/>
    <stop offset=".08"  stop-color="#96581A"/>
    <stop offset=".2"   stop-color="#4A2408"/>
    <stop offset=".5"   stop-color="#B96F26"/>
    <stop offset=".72"  stop-color="#7A4212"/>
    <stop offset=".87"  stop-color="#EBAC55"/>
    <stop offset=".95"  stop-color="#FBE2B4"/>
    <stop offset="1"    stop-color="#33 1A04"/>
  </linearGradient>
  <linearGradient id="accordV" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"   stop-color="#000" stop-opacity=".18"/>
    <stop offset=".55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1"   stop-color="#180800" stop-opacity=".55"/>
  </linearGradient>
  <radialGradient id="chalo" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#C98A3A" stop-opacity=".42"/>
    <stop offset="1"   stop-color="#8A4E14" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cshade" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#000" stop-opacity=".9"/>
    <stop offset=".55" stop-color="#000" stop-opacity=".36"/>
    <stop offset="1"   stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="cpool" cx=".5" cy=".5" r=".5">
    <stop offset="0"   stop-color="#FFCE8A" stop-opacity=".7"/>
    <stop offset=".4"  stop-color="#B8701F" stop-opacity=".26"/>
    <stop offset="1"   stop-color="#7A4410" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="pip" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0"   stop-color="#1A1208" stop-opacity=".8"/>
    <stop offset=".22" stop-color="#8A7048" stop-opacity=".7"/>
    <stop offset=".55" stop-color="#3A2C18" stop-opacity=".55"/>
    <stop offset=".82" stop-color="#FFF3D8" stop-opacity=".9"/>
    <stop offset="1"   stop-color="#2A1F10" stop-opacity=".7"/>
  </linearGradient>
  <filter id="c2" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="2"/></filter>
  <filter id="c6" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="c16" x="-85%" y="-85%" width="270%" height="270%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="c50" x="-95%" y="-95%" width="290%" height="290%"><feGaussianBlur stdDeviation="50"/></filter>
  <filter id="cgrain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="6"/></filter>
  <clipPath id="cinner"><rect x="{gx+10}" y="{gt}" width="{gw-20}" height="{gb-gt-14}" rx="18"/></clipPath>
</defs>

<ellipse cx="{CX}" cy="900" rx="360" ry="440" fill="url(#chalo)" style="mix-blend-mode:screen"/>
<ellipse cx="{CX}" cy="{gb+14}" rx="250" ry="40" fill="url(#cshade)"/>
<ellipse cx="{CX+34}" cy="{gb+8}" rx="170" ry="26" fill="url(#cpool)" style="mix-blend-mode:screen"/>

<!-- ── the pipette, held above ── -->
<g transform="translate({CX+16},300) rotate(9)">
  <rect x="-15" y="-260" width="30" height="86" rx="14" fill="#241A0C"/>
  <rect x="-15" y="-260" width="11" height="86" fill="#0E0A06" opacity=".5"/>
  <rect x="4" y="-254" width="7" height="74" rx="3.5" fill="#B8A484" opacity=".8" filter="url(#c2)"/>
  <rect x="-11" y="-178" width="22" height="330" rx="11" fill="url(#pip)"/>
  <rect x="-6" y="-120" width="12" height="220" rx="6" fill="#B96F26" opacity=".85"/>
  <rect x="3" y="-172" width="5" height="318" rx="2.5" fill="#FFF6E4" opacity=".85" filter="url(#c2)"/>
  <path d="M-11 152 L0 196 L11 152 Z" fill="url(#pip)"/>
  <ellipse cx="0" cy="176" rx="6" ry="11" fill="#D9963F" opacity=".95"/>
</g>
<!-- the drop, on its way down -->
<ellipse cx="{CX+46}" cy="560" rx="11" ry="17" fill="#EBAC55" opacity=".95" filter="url(#c2)"/>
<ellipse cx="{CX+46}" cy="560" rx="46" ry="52" fill="#C98A3A" opacity=".4" filter="url(#c16)" style="mix-blend-mode:screen"/>

<!-- ── the glass ── -->
<g clip-path="url(#cinner)">
  <rect x="{gx}" y="{liq}" width="{gw}" height="{gb-liq}" fill="url(#accord)"/>
  <rect x="{gx}" y="{liq}" width="{gw}" height="{gb-liq}" fill="url(#accordV)"/>
  <ellipse cx="{CX+60}" cy="{liq+150}" rx="120" ry="120" fill="#FFCE8A" opacity=".22" filter="url(#c16)"/>
  <ellipse cx="{CX-140}" cy="{liq+180}" rx="130" ry="150" fill="#000" opacity=".45" filter="url(#c16)"/>
</g>
<!-- the surface of the accord, and the ring it left as it filled -->
<ellipse cx="{CX}" cy="{liq}" rx="{gw/2-10}" ry="30" fill="#C4832C"/>
<ellipse cx="{CX}" cy="{liq}" rx="{gw/2-10}" ry="30" fill="none" stroke="#FFE2AE" stroke-width="2" opacity=".55"/>
<ellipse cx="{CX+52}" cy="{liq-9}" rx="66" ry="11" fill="#FFEFD2" opacity=".5" filter="url(#c6)"/>
{''.join(f'<line x1="{gx+14}" y1="{y}" x2="{gx+52}" y2="{y}" stroke="#F2E2C0" stroke-width="2.5" opacity=".3"/>' for y in range(880, 1250, 62))}

<!-- the glass wall over it all -->
<rect x="{gx}" y="{gt}" width="{gw}" height="{gb-gt}" rx="20" fill="url(#cglass)"/>
<rect x="{gx}" y="{gt}" width="{gw}" height="{gb-gt}" rx="20" fill="none" stroke="#7A6444" stroke-width="2" opacity=".55"/>
<ellipse cx="{CX}" cy="{gt}" rx="{gw/2}" ry="26" fill="none" stroke="#EFE0BE" stroke-width="4" opacity=".55" filter="url(#c2)"/>
<path d="M{CX-40} {gt-24} A {gw/2} 26 0 0 1 {gx+gw-8} {gt-4}" stroke="#FFFDF6" stroke-width="6"
      fill="none" opacity=".9" filter="url(#c2)"/>
<rect x="{gx+gw-13}" y="{gt+40}" width="6" height="{gb-gt-110}" rx="3" fill="#FFF8E8" opacity=".8" filter="url(#c2)"/>
<rect x="{gx+8}" y="{gt+70}" width="4" height="{gb-gt-180}" rx="2" fill="#E8D2A8" opacity=".3" filter="url(#c2)"/>
<ellipse cx="{CX}" cy="{gb-22}" rx="112" ry="20" fill="#FFDDA2" opacity=".4" filter="url(#c6)"/>

<g style="mix-blend-mode:overlay" opacity=".05"><rect width="{W}" height="{H}" filter="url(#cgrain)"/></g>
</svg>'''


if __name__ == '__main__':
    import sys, xml.etree.ElementTree as ET
    svg = build().replace('#33 1A04', '#331A04')
    ET.fromstring(svg)
    open(sys.argv[1], 'w', encoding='utf-8').write(svg)
    print('compose.svg written')
