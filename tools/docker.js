import util from 'util';
import { exec as cbExec } from 'child_process';

export const exec = util.promisify(cbExec);

export async function getContainerId() {
  process.stdout.write('Getting discovery container id...');
  const { stdout, stderr } = await exec('docker ps | grep discovery');
  const out = stdout.trim().split('\n');
  let id = null;

  if (out.length > 0) {
    id = out[0].trim().split(' ')[0];
  }

  return id;
}

export async function copyToContainer(container, src, dst) {
  console.log(`Copying ${src} to ${container}:${dst} ...`);
  const { stdout, stderr } = await exec(`docker cp ${src} ${container}:${dst}`);
}
