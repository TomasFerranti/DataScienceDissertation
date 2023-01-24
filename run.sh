xhost +
docker-compose up -d
docker exec -ti interface python interface.py
docker-compose down
xhost -