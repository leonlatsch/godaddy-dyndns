FROM python:alpine3.19

RUN mkdir /config
ADD requirements.txt /requirements.txt
ADD godaddy-dyndns.py /godaddy-dyndns.py
ADD godaddy-dyndns.conf /config/godaddy-dyndns.conf

RUN pip3 install -r requirements.txt
RUN chmod +x /godaddy-dyndns.py

CMD [ "/godaddy-dyndns.py" ]