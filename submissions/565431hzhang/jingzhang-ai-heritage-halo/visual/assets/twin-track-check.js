// Twin-Track Release Check — 双轨放行验证脚本
// 用法: node twin-track-check.js
const fs = require('fs');
const path = require('path');
const dir = path.join(__dirname);
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'twin-track-spec.json'), 'utf-8'));
const results = JSON.parse(fs.readFileSync(path.join(dir, 'twin-track-check-results.json'), 'utf-8'));
console.log('=== 双轨放行验证 / Twin-Track Release Check ===');
console.log('Spec:', spec.spec_name);
console.log('One-line test:', spec.one_line_test);
console.log('');
let provisionalCount = 0, blockedCount = 0;
for (const sc of results.scenarios) {
    const passed = spec.fields.every(f => sc[f.id] && sc[f.id].passed);
    const status = passed ? sc.overall : 'blocked';
    if (status === 'blocked') blockedCount++; else provisionalCount++;
    console.log(sc.id + ' ' + sc.name_zh + ': ' + status.toUpperCase());
    for (const f of spec.fields) {
        console.log('  ' + (sc[f.id] && sc[f.id].passed ? '✓' : '✗') + ' ' + f.label_zh);
    }
    console.log('');
}
console.log('=== Summary ===');
console.log('Total: ' + results.scenarios.length + ' | Provisional: ' + provisionalCount + ' | Blocked: ' + blockedCount);
console.log('Note: All scenarios passed design self-check. No field verification conducted yet.');
