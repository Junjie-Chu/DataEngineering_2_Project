FROM python:3.6
ADD requirements.txt /app/requirements.txt
COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
ENTRYPOINT ["python"]
CMD ["./development_server/scriptModels.py"]
