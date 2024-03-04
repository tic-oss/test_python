# python

## postgres 
docker compose -f postgresql.yml down
docker compose -f postgresql.yml up

## jhispter-resgitry 

docker compose -f jhipster-registry.yml down
docker compose -f jhipster-registry.yml up

## application 

docker compose --network=host -p8001:8001 fastapi -d  
(-d for detach mode)