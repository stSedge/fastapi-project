#'''FROM python:3.11-slim
#WORKDIR /app
#COPY pyproject.toml poetry.lock* ./
#RUN pip install poetry
#RUN poetry install --no-dev
#COPY . .
#CMD ["poetry", "run", "uvicorn", "java_luchshe.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]'''

FROM python:3.11.2-buster
ENV DEBIAN_FRONTEND='noninteractive'
RUN apt-get update && apt install -y curl libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH="${PATH}:/root/.local/bin"
COPY ./java_luchshe /app/java_luchshe
COPY migration /app/migration
COPY alembic.ini /app/
COPY pyproject.toml /app/
ENV PYTHONPATH /app/
WORKDIR /app
RUN poetry config virtualenvs.create false \
    && poetry install --no-root
RUN chmod +x ./java_luchshe/start.sh
EXPOSE 8000