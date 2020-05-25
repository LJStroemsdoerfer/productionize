            FROM python:3.7.7
            RUN mkdir -p /api
            COPY api.py /api/api.py
            COPY requirements.txt /api/requirements.txt
            RUN python -m pip install -r /api/requirements.txt
            EXPOSE 8000
            ENTRYPOINT ["python", "api/api.py"]            