# Troubleshoot

This page presents users and devs alike with an amalgam of quick fixes for the various issues we ran into.

## Docker

### Reset
**Docker remove all images:**
`docker rmi $(docker images -a -q)`
**Docker remove all Containers:**
`docker stop $(docker ps -a -q)`
`docker rm $(docker ps -a -q)`
**Docker remove all volumes:**
`docker volume rm $(docker volume ls -f)`

### Reset \#2
**Docker remove all except volumes:**
`sudo docker system prune`
**Docker remove all volumes:**
`sudo docker volume prune`

### Docker won't build without super user permissions

1. Add the docker group if it doesn't already exist:
```
sudo groupadd docker
```
2. Add the $USER you'd like to use to the docker group
```
sudo gpasswd -a $USER docker
```
3. a. Log yourself into the new docker group:
```
newgrp docker
```
3. b. Log out and log in to the user you just added to the docker group.
4. Test if you can run docker without su privileges by typing:
```
docker run hello-world
```

---

## PostgreSQL

### DB reset

In root directory
```./cjlean db-reset```

### DB reset alternative
1.  Get into postgres container:
`docker exec -it <CONTAINER_ID> bash`
2.  Enter postgres command line:
`psql postgres postgres` (if asked for password enter DEV_PASS_NOT_SECRET)
3.  Type in order:
`DROP SCHEMA public CASCADE;`
`CREATE SCHEMA public;`
`GRANT ALL ON SCHEMA public TO postgres;`
`GRANT ALL ON SCHEMA public TO public;`
4.  Type:
`\q` to exit psql

## Environment variable errors

1. Ensure when building that you did not build with root
2. Ensure the environment variables are set up in ~/.bashrc
3. If you built with root, ```./cjl clean``` with root and ```./cjl build --no-cache``` out of root


---

We've noticed that sometimes the database takes ~30 sec to create the models at runtime and be ready to accept connections, but the application services have thrown an error due to the requirement of creating a database connection. If you simply `./cjl down && ./cjl up`, this problem goes away, but it may be worth having the application servers stall and wait as they perform a health check on the database before attempting to create a database connections.


