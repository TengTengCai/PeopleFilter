FROM python:2
ENV PYTHONPATH=.
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
