Title: A tidbit about docker containers
Date: 2024-04-02 18:30
Category: TILs
Status: published

I played around with docker containers today. Tried to install mssql on an M2 mac. Didn't go smoothly at first, but I attribute it to inexperience. The arm architecture crops up here and there when you're on one of those. Anyway, cool thing:

You can run a terminal inside a docker container by using `docker exec -it <container-name> bash`. I thought it was pretty neat.