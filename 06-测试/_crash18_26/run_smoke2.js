const path = require('path');
const { runSmoke } = require(path.resolve(process.argv[2]));
runSmoke(process.argv[3]).then(function (r) {
  console.log(r.out.join('\n'));
  process.exit(r.ok ? 0 : 1);
}, function (e) { console.error(e && e.stack || e); process.exit(2); });
