const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const ROOT=path.resolve(__dirname,'..','..');
const file=path.join(ROOT,'manifest.json');
const manifest=JSON.parse(fs.readFileSync(file,'utf8'));
const sha=rel=>crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT,rel))).digest('hex');

manifest.files=manifest.files.filter(item=>fs.existsSync(path.join(ROOT,item.path)));
for(const item of manifest.files)if(item.path==='manifest.json')delete item.sha256;
const entries=[
  ['visual/assets/spatial-decision.json','evidence_data',true,'neutral'],
  ['visual/assets/tabletop-results.json','evidence_data',false,'neutral'],
  ['visual/assets/red-team-review.json','evidence_data',true,'neutral'],
  ['visual/assets/spatial-audit-v11.js','verification_script',false,'neutral'],
  ['visual/assets/content-v11.js','verification_script',false,'neutral'],
  ['visual/assets/build-v11.js','verification_script',false,'neutral'],
  ['visual/assets/build-v11-html.js','verification_script',false,'neutral'],
  ['visual/assets/qa-v11.js','verification_script',false,'neutral'],
  ['visual/assets/register-v11-manifest.js','verification_script',false,'neutral'],
  ['visual/assets/v11.css','asset',true,'neutral'],
  ['visual/assets/v11.js','asset',true,'neutral'],
];
for(const base of ['spatial-alternatives','s7-detail-v11','s7-section-node-v11']){
  entries.push([`assets/figures/${base}.png`,'proposal_figure',true,'zh']);
  entries.push([`assets/figures/${base}.en.png`,'proposal_figure',true,'en',`assets/figures/${base}.png`]);
}
for(const [rel,role,required,language,translation_of] of entries){
  if(!fs.existsSync(path.join(ROOT,rel)))throw new Error(`Cannot register missing V11 file: ${rel}`);
  manifest.files=manifest.files.filter(x=>x.path!==rel);
  const item={path:rel,role,required,language,sha256:sha(rel)};
  if(translation_of)item.translation_of=translation_of;
  manifest.files.push(item);
}
manifest.files.sort((a,b)=>a.path.localeCompare(b.path));
fs.writeFileSync(file,JSON.stringify(manifest,null,2)+'\n');
console.log(`V11 manifest registered: ${manifest.files.length} existing files`);
