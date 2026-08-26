const fs = require('fs');
const path = require('path');
const { PNG } = require(path.resolve(__dirname, '../frontend/node_modules/pngjs'));

const inputPath = path.resolve(__dirname, '../Logo/logo.png');
const publicOutputPath = path.resolve(__dirname, '../frontend/public/logo-dark.png');
const srcOutputPath = path.resolve(__dirname, '../frontend/src/assets/logo-dark.png');

const data = fs.readFileSync(inputPath);
const png = PNG.sync.read(data);

for (let y = 0; y < png.height; y++) {
  for (let x = 0; x < png.width; x++) {
    const idx = (png.width * y + x) << 2;
    const a = png.data[idx + 3];

    if (a > 10) {
      // Make entire logo complete pure white
      png.data[idx] = 255;
      png.data[idx + 1] = 255;
      png.data[idx + 2] = 255;
    }
  }
}

const buffer = PNG.sync.write(png);
fs.writeFileSync(publicOutputPath, buffer);
fs.writeFileSync(srcOutputPath, buffer);
console.log('SUCCESS: Generated 100% pure white logo-dark.png!');
