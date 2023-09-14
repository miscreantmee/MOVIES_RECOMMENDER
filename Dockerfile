FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python main.py
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]