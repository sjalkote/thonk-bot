sudo systemctl start docker
sleep 1

docker stop thonk-bot
sleep 2

docker container rm thonk-bot
docker container ls
sleep 1

docker image rm thonk-bot
echo 'Removed old thonk-bot images!'
sleep 1

docker build -t thonk-bot .
echo 'Docker image succesfully built!'
sleep 1

docker images
sleep 2
echo 'Running newly generated Docker image in container!'

docker run --name thonk-bot -it thonk-bot launcher.py
