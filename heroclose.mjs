import {chromium} from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--no-sandbox']});
for (const w of [1800,1440]){
  const p=await (await b.newContext({viewport:{width:w,height:900}})).newPage();
  await p.goto('http://127.0.0.1:8099/index.html?lang=el',{waitUntil:'domcontentloaded'});
  await p.waitForTimeout(6300);
  await p.evaluate(()=>document.querySelectorAll('.scene').forEach((s,k)=>s.classList.toggle('on',k===0)));
  await p.waitForTimeout(900);
  await p.screenshot({path:`close-${w}.png`});
  console.log(w,'shot');
  await p.close();
}
await b.close();
