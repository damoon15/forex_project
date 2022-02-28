docker build . -t forex
docker run -d -p 8000:8000 -t -i forex:latest
