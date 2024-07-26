FROM python:3.8.10
COPY . /
WORKDIR /
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 9999
ENTRYPOINT [ "python3" ]
CMD [ "recom_service.py" ]