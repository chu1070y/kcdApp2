FROM python:3.10.9

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN echo Asia/Seoul > /etc/timezone

WORKDIR /kcdapp2

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD python main.py
