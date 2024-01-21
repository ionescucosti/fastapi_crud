# build container
docker build -t app .

# run container
docker run -p 80:80 app