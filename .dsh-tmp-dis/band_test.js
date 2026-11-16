
const fs = require("fs");
const src = fs.readFileSync(process.argv[2], "utf8").replace(/\r/g, "");
const i = src.indexOf("function updateBandFromNodes()");
const j = src.indexOf("\n}", i);
const fn = src.slice(i, j + 2);
console.log("---- fn ----\n" + fn + "\n");
global.syncBandUI = function () {};
function run(nodes, geo) {
  global.S = { nodes: nodes, geo: geo, band: { on: false, lo: 0, hi: 0 }, bandTouched: false, bandMin: 0, bandMax: 0 };
  eval(fn);
  updateBandFromNodes();
  return { lo: S.band.lo, hi: S.band.hi, min: S.bandMin, max: S.bandMax };
}
const geo = { hdr: { bbox: [[-20.05, 0, -20.05], [20.05, 3, 20.05]] } };
console.log("empty+geo :", JSON.stringify(run([], geo)));
console.log("empty+nogeo:", JSON.stringify(run([], null)));
console.log("nodes     :", JSON.stringify(run([{ p: [0, 1.5, 0] }, { p: [3, 1.5, 2] }], geo)));
