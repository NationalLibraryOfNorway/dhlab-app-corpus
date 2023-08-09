FROM python:3.11-slim
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY app/ .
CMD streamlit run app.py --browser.gatherUsageStats=False --server.baseUrlPath /korpus
