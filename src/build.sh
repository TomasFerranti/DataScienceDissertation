# TextureExtractor
cd TextureExtractor
## Get three.js
mkdir -p app/public/packages
cd app/public/packages
wget https://github.com/mrdoob/three.js/archive/master.zip
unzip master.zip
rm master.zip
cd ../../..
## Build docker image
docker build --rm -t server:latest .

# SMTools
cd ../SMTools
## Build docker image
docker build --rm -t interface:latest .