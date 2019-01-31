import { spawn } from 'child_process';
import { exec, getContainerId } from './docker';

// enter docker container shell
async function shell() {
  try {
    const containerId = await getContainerId();
    if (containerId) {
      console.log(':', containerId);
    } else {
      console.log(': Not found!!');
      return;
    }
  
    const p = spawn(`docker exec -it ${containerId} env TERM=xterm-256color bash`);
    p.stdout.on('data', data => {
      console.log(data.toString());
    });
    p.stderr.on('data', data => {
      console.log(data.toString());
    });
    p.on('exit', code => {
      console.log(`Shell exited with code ${code}`);
      process.exit(code);
    });
    p.on('error', e => {
      console.log('Error is occured:', e);
    });
  } catch(e) {
    console.log('shell is failed:', e);
  }
}

export default shell;
