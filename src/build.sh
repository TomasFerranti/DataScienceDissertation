# TextureExtractor
cd TextureExtractor
## Get three.js
mkdir -p public/packages
cd public/packages
wget https://github.com/mrdoob/three.js/archive/master.zip
unzip master.zip
rm master.zip
cd ../..
## Build docker image
docker build --rm -t server:latest .

# SMTools
cd ../SMTools
## Build docker image
docker build --rm -t interface:latest .