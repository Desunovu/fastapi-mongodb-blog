FROM python:3.11-alpine
COPY . ./backend
WORKDIR ./backend
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "blogapp.main:app", "--host", "0.0.0.0"]