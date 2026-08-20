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
  ['visual/assets/v14-spatial-model.json','evidence_data',true,'neutral'],
  ['visual/assets/content-v14.js','verification_script',false,'neutral'],
  ['visual/assets/build-v14.js','verification_script',false,'neutral'],
  ['visual/assets/build-v14-html.js','verification_script',false,'neutral'],
  ['visual/assets/qa-v14.js','verification_script',false,'neutral'],
  ['visual/assets/register-v14-manifest.js','verification_script',false,'neutral'],
  ['assets/media/verification-ring-v14.webp','media_poster',false,'neutral'],
  ['assets/media/verification-ring-v14.jpg','media_poster',false,'neutral'],
  ['assets/media/translation-gate-v14.webp','media_poster',false,'neutral'],
  ['assets/media/translation-gate-v14.jpg','media_poster',false,'neutral'],
  ['assets/media/receipt-porch-v14.webp','media_poster',false,'neutral'],
  ['assets/media/receipt-porch-v14.jpg','media_poster',false,'neutral'],
];

for(const [rel,role,required,language,translation_of] of entries){
  if(!fs.existsSync(path.join(ROOT,rel)))throw new Error(`Cannot register missing V14 file: ${rel}`);
  manifest.files=manifest.files.filter(item=>item.path!==rel);
  const item={path:rel,role,required,language,sha256:sha(rel)};
  if(translation_of)item.translation_of=translation_of;
  manifest.files.push(item);
}

manifest.files.sort((a,b)=>a.path.localeCompare(b.path));
fs.writeFileSync(file,JSON.stringify(manifest,null,2)+'\n');
console.log(`V14 manifest additions registered: ${manifest.files.length} existing files`);
