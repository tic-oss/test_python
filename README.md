 
# run Eureka server ,using this command:  (server protected by keycloak)
         
         docker compose -f fastapi/docker/jhipster-registry-with-kp.yml up 
         docker compose -f fastapi/docker/jhipster-registry-with-kp.yml down 

 # run keycloak, using this command:   

         docker compose -f fastapi/docker/keycloak.yml up 
         docker compose -f fastapi/docker/keycloak.yml down      

# or run both keycloak & eureka server in stack using this command: (path : cd fastapi/)

         docker compose -f fastapi/docker/services.yml up 
         docker compose -f fastapi/docker/services.yml down 

                    or 

 # for run eureka server (without keycloak protection):     
         docker compose -f fastapi/docker/jhipster-registry.yml up 
         docker compose -f fastapi/docker/jhipster-registry.yml down 


# for standalone version keycloak: (cd Downloads/keycloak-23.0.3/bin)         
        ./kc.sh start-dev    
  

  ---------------------------------------------------------------------------

# run  rabbitmq server using this command: 

                      docker run -d --name my-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management


 # run microservice-1 (posts) using this command: (path : cd fastapi/posts)
                              uvicorn main:app --port 9001

or

                            uvicorn main:app --host 0.0.0.0 --port 9001
 
 # run microservice-2 (slack) using this command:  (path : cd fastapi/slack)

                             uvicorn main:app --port 9000

or 

                                    python main.py

# run databases using this commands :

   
   # 1. create network in docker using this command: 

                                 docker network create my_network

   # 2. run postgres, using this command:

                      docker run -d  --name mongodb  -p 27017:27017 --network my_network mongo:latest

   # 3. run mongo db, using this command:

                  docker run -d --name postgresql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pass123 -e POSTGRES_DB=python -p 5432:5432 --network my_network  postgres:latest

or 

   # 1. run postgres, using this command:

                      docker run -d  --name host_mongodb  -p 27017:27017 --network=host mongo:latest


   # 2. run mongo db, using this command:

                  docker run -d --name host_postgresql -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=pass123 -e POSTGRES_DB=python -p 5432:5432 --network=host  postgres:latest
