docker stop thonk-bot
TIMEOUT 2

docker container rm thonk-bot
docker container ls
TIMEOUT 2

docker image rm thonk-bot
echo "Removed old thonk-bot images!"
TIMEOUT 1

docker build -t thonk-bot .
echo "Docker image successfully built!"
TIMEOUT 1

docker images
TIMEOUT 2
echo "Running newly generated Docker image in container!"

docker run --name thonk-bot -it thonk-bot launcher.py
