// Celadon & Frond Theme — celadon mint and lavender foliage
import { readFile } from 'node:fs/promises';

const PALETTE = {
  celadon: '#C1E6D4',
  deepCeladon: '#173A33',
  lavender: '#BAC0E3',
  purple: '#C79AD4',
  peach: '#E8CFC0',
  cream: '#E6E8D2',
};

export class Frond {
  constructor(grove = 'North alcove') {
    this.grove = grove;
    this.palette = PALETTE;
    this.leaves = Object.keys(PALETTE).filter((k) => k !== 'cream');
  }

  blend(from, to, ratio = 0.5) {
    const parse = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    const [a, b] = [parse(from), parse(to)];
    return '#' + a.map((v, i) => Math.round(v * (1 - ratio) + b[i] * ratio)
      .toString(16).padStart(2, '0')).join('');
  }

  async readGrove(file) {
    const content = await readFile(file, 'utf8');
    return { grove: this.grove, leaves: this.leaves.length,
             lines: content.split('\n').filter(Boolean).length, content };
  }
}

const frond = new Frond();
console.log(`shade: ${frond.blend(PALETTE.celadon, PALETTE.lavender)}`);
