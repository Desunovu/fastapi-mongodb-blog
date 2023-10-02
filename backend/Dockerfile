FROM python:3.11-alpine
RUN mkdir backend
WORKDIR /backend
COPY /backend/pyproject.toml .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY /backend /backend
EXPOSE 8000
CMD ["uvicorn", "blogapp.main:app", "--host", "0.0.0.0"]