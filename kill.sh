sudo ip addr delete 192.168.255.254/16 dev lo
docker-compose kill
docker-compose rm -f
docker volume rm supsnapserver_db -f
