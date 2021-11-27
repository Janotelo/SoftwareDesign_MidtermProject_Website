FROM python
RUN pip install flask
RUN pip install requests
COPY  ./templates /home/myapp/templates/
COPY  ./static /home/myapp/static/
COPY  LoginSystem.py /home/myapp/
EXPOSE 5001
CMD python3 /home/myapp/LoginSystem.py
