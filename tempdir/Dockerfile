FROM python
RUN pip install flask
COPY  ./templates /home/myapp/templates/
COPY  ./static /home/myapp/static/
COPY  ./image /home/myapp/image/
COPY  LoginSystem.py /home/myapp/
EXPOSE 8080
CMD python3 /home/myapp/LoginSystem.py
