const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '../frontend');

const emojiRegex = /[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F1E6}-\u{1F1FF}]|[\u{1F600}-\u{1F64F}]|[\u{1F680}-\u{1F6FF}]|[\u{1F900}-\u{1F9FF}]|[\u{1FA70}-\u{1FAFF}]|[\u{200D}]|[\u{FE0F}]|[⚡🚀🛡✨🔒📦🤖💳📈💬🏢⚠✓✗]/gu;

function scanDir(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (file === 'node_modules' || file === 'dist' || file === '.git') continue;
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      scanDir(fullPath);
    } else if (/\.(tsx|ts|jsx|js|html|css|json)$/.test(file)) {
      const content = fs.readFileSync(fullPath, 'utf8');
      const lines = content.split('\n');
      lines.forEach((line, idx) => {
        const matches = line.match(emojiRegex);
        if (matches && matches.length > 0) {
          console.log(`${path.relative(rootDir, fullPath)}:${idx + 1} -> ${line.trim()}`);
        }
      });
    }
  }
}

scanDir(rootDir);
