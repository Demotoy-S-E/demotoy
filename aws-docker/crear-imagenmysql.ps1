# delete the old image and create a new one
docker rmi mysql-image-service
docker build -f Dockerfile-Mysql -t mysql-image-service .
# docker exec -it mysql-service mysql -u adminuser -p adminuser

# docker-compose up
# docker-compose down