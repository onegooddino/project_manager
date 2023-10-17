Username    Password

#admin
dino        dino;pass

#employee
emp1        emp1;pass

#manager
mng1        manager;pass

#Build docker image
docker build -t project_manager . 

#run docker image
docker run -d -p 8000:8000 --name project_manager project_manager
