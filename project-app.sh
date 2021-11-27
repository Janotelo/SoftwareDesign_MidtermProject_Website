#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp LoginSystem.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.
cp -r image/* tempdir/image/.

echo "FROM python" > tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./image /home/myapp/image/" >> tempdir/Dockerfile
echo "COPY  LoginSystem.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/LoginSystem.py" >> tempdir/Dockerfile

cd tempdir
docker build -t projectapp .
docker run -t -d -p 8080:8080 --name projectrunning projectapp
docker ps -a