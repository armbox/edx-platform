import fs from 'fs';
import { readFile } from './lib/fs';
import { getContainerId, copyToContainer } from './docker';

// copy .git directory to docker container
async function git() {
  const containerId = await getContainerId();
  if (containerId) {
    console.log(':', containerId);
  } else {
    console.log(': Not found!!');
    return;
  }

  let gitFolder = '.git';
  if (fs.existsSync(gitFolder) && fs.lstatSync(gitFolder).isFile()) {
    const file = await readFile(gitFolder);
    gitFolder = file.split(':')[1].trim();
  }

  await copyToContainer(containerId, gitFolder, '/edux/course-discovery/.git');
}

export default git;
