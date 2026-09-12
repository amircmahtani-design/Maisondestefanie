import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
const [,, listFile] = process.argv;
const jobs = JSON.parse(fs.readFileSync(listFile,'utf8'));  // [{svg,out,w,h,opaque}]
const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args:['--no-sandbox','--force-color-profile=srgb','--disable-lcd-text']});
for (const j of jobs){
  const ctx = await b.newContext({viewport:{width:j.w,height:j.h},deviceScaleFactor:1});
  const p = await ctx.newPage();
  const svg = fs.readFileSync(j.svg,'utf8');
  await p.setContent(`<style>html,body{margin:0;padding:0;background:transparent}
    svg{display:block;width:${j.w}px;height:${j.h}px}</style>${svg}`,{waitUntil:'load'});
  await p.waitForTimeout(420);
  fs.mkdirSync(path.dirname(j.out),{recursive:true});
  await p.screenshot({path:j.out, omitBackground:!j.opaque});
  await ctx.close();
  console.log('rendered', j.out);
}
await b.close();
