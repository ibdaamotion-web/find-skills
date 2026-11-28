// render each text card to a transparent 1080-wide PNG with Chromium (correct Arabic shaping)
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
 const [,,jobs,outdir]=process.argv; const items=JSON.parse(fs.readFileSync(jobs));
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:700},deviceScaleFactor:1});
 for(const it of items){
  const lines=it.text.split('|').map(l=>`<div>${l}</div>`).join('');
  await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=Amiri:wght@700&family=Reem+Kufi:wght@500;700&display=block" rel="stylesheet">
  <style>html,body{margin:0;background:transparent}#c{width:1080px;padding:60px 70px;box-sizing:border-box;direction:rtl;text-align:center;
  font-family:${it.font||"'Aref Ruqaa'"};font-size:${it.size||66}px;line-height:1.45;color:${it.color||'#FFF6E6'};
  text-shadow:0 0 3px rgba(0,0,0,.9),0 2px 6px rgba(0,0,0,.9),0 0 22px rgba(0,0,0,.85),0 0 44px rgba(0,0,0,.7),0 0 16px rgba(255,190,90,.35)}</style></head>
  <body><div id="c">${lines}</div></body></html>`);
  await p.evaluate(()=>document.fonts.ready);
  const el=await p.$('#c'); await el.screenshot({path:`${outdir}/${it.id}.png`,omitBackground:true});
 }
 await b.close();})();
