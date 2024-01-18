# read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# you will also find guides on how best to write your Dockerfile

FROM python:3.9.18

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

RUN mkdir /.cache && chmod 777 /.cache

COPY ./routers /code/routers

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
CMD ["uvicorn", "routers.text_models:app", "--host", "0.0.0.0", "--port", "8080"]
