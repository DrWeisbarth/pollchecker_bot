FROM python:3.9
WORKDIR ./poll_checker_project
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY mongodb.py .
COPY poll_parser.py .
CMD ["python","main.py"]