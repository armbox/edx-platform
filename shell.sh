container=$(node ./tools/container.js $1)
docker exec -it ${container} env TERM=xterm-256color bash 
