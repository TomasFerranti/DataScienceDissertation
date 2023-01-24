# Install three.js
rm -rf src/TextureExtractor/app/public/packages
mkdir src/TextureExtractor/app/public/packages
cd src/TextureExtractor/app/public/packages
wget https://github.com/mrdoob/three.js/archive/master.zip
unzip master.zip
rm master.zip
cd ../../../../..

# Build dockers images
docker-compose build