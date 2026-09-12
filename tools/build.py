import json, re, sys, importlib, xml.etree.ElementTree as ET
for m in ('kit','s_rooms','s_objects','s_bottle'): sys.modules.pop(m, None)
import s_rooms, s_objects, s_bottle
SPECS=[('hero-still', lambda: s_rooms.hero_still(2400,1350), 2400,1350, True),
       ('workshop',   lambda: s_rooms.workshop(2400,1030),   2400,1030, True),
       ('atwork',     lambda: s_rooms.atwork(2400,1030),     2400,1030, True),
       ('counter',    lambda: s_rooms.counter_panel(900,1125), 900,1125, True),
       ('botanical',  lambda: s_rooms.botanical_panel(900,1125),900,1125, True),
       ('bench',      lambda: s_rooms.bench_panel(900,1125), 900,1125, True),
       ('sealing',    lambda: s_rooms.sealing_panel(900,1125),900,1125, True),
       ('shopfront',  lambda: s_rooms.shopfront(900,1125),   900,1125, True),
       ('plaka',      lambda: s_rooms.plaka_panel(900,1125), 900,1125, True),
       ('bottle',     s_bottle.build,                         900,1200, False),
       ('vessel',     lambda: s_objects.vessel(1200,900),    1200,900,  False),
       ('rose',       lambda: s_objects.rose(1200,900),      1200,900,  False)]
jobs=[]
for n,fn,w,h,opaque in SPECS:
    svg=fn()
    bad={c for c in re.findall(r'(?:fill|stroke|stop-color)="([^"]+)"', svg)
         if c.startswith('#') and not re.fullmatch(r'#[0-9A-Fa-f]{3,8}', c)}
    if bad: print(n,'BAD COLOUR:',bad)
    try: ET.fromstring(svg)
    except Exception as e: print(n,'XML ERROR:',e); continue
    open(f'scenes/{n}.svg','w',encoding='utf-8').write(svg)
    jobs.append({"svg":f"scenes/{n}.svg","out":f"render/{n}.png","w":w,"h":h,"opaque":opaque})
json.dump(jobs, open('jobs.json','w'))
print('built', len(jobs), 'scenes')
