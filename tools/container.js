const util = require('util');
const exec = util.promisify(require('child_process').exec);
const mode = process.env.SMARTLEARN_MODE;

async function getContainerId(sys = 'lms') {
  const { stdout, stderr } = await exec(`docker ps | grep ${mode}_edux-${sys}`);
  const out = stdout.trim().split('\n');
  let id = null;

  if (out.length > 0) {
    id = out[0].trim().split(' ')[0];
  }

  console.log(id);
}

if (require.main === module) {
  getContainerId(process.argv[2]);
}
