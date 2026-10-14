const path = require('path');
const { runSmoke } = require(path.resolve('06-测试/death-diag-stub/smoke_death_diag.js'));
runSmoke(process.argv[2]).then(function (r) {
  console.log(r.out.join('\n'));
  process.exit(r.ok ? 0 : 1);
}, function (e) { console.error(e && e.stack || e); process.exit(2); });
