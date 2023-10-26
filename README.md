
#Build docker image
docker build -t project_manager . 

#run docker image
docker run -d -p 8000:8000 --name project_manager project_manager
