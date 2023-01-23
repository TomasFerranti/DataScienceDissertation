xhost +
cd TextureExtractor
docker run --name server -p 8000:8000/tcp -v $PWD/app:/TextureExtractor/app:Z -v $PWD/../../images:/TextureExtractor/app/public/images:Z -v $PWD/../../calib:/TextureExtractor/app/public/calib:Z -d server:latest
cd ../SMTools
docker run --net=host -e DISPLAY --name interface -ti -v $PWD:/SMTools:Z -v $PWD/../../images:/SMTools/images:Z -v $PWD/../../calib:/SMTools/calib:Z interface:latest
docker container stop interface
docker container stop server
docker container rm interface
docker container rm server
xhost -