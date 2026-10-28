const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const htmlPath = path.join(__dirname, 'ac-stock-tracker.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)];

if (!scripts.length) {
  throw new Error('No inline scripts found in ac-stock-tracker.html');
}

for (let index = 0; index < scripts.length; index += 1) {
  const tempPath = path.join(os.tmpdir(), `ac-stock-inline-${process.pid}-${index}.js`);
  fs.writeFileSync(tempPath, scripts[index][1], 'utf8');
  const result = spawnSync(process.execPath, ['--check', tempPath], { stdio: 'inherit' });
  try {
    fs.unlinkSync(tempPath);
  } catch (_) {}
  if (result.status !== 0) {
    process.exit(result.status || 1);
  }
}

console.log(`node --check passed for ${scripts.length} inline script(s)`);
