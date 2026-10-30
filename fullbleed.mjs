import {chromium,devices} from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args:['--no-sandbox']});
for (const [tag,w,h,mob] of [['d',1800,900,false],['l',1440,900,false],['m',390,844,true]]){
  const p=await (await b.newContext({viewport:{width:w,height:h},...(mob?{userAgent:devices['iPhone 13'].userAgent,hasTouch:true}:{})})).newPage();
  const bad=[]; p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url().split('/').pop());});
  await p.goto('http://127.0.0.1:8099/index.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(6300);
  for (let i=0;i<4;i++){
    await p.evaluate(j=>document.querySelectorAll('.scene').forEach((s,k)=>s.classList.toggle('on',k===j)),i);
    await p.waitForTimeout(800);
    await p.screenshot({path:`FB-${tag}-${i}.png`});
  }
  console.log(tag, await p.evaluate(()=>[...document.querySelectorAll('.scene .lay.a')].map(i=>(i.currentSrc||'').split('/').pop()).join(' ')), bad.length?bad:'clean');
  await p.close();
}
await b.close();
