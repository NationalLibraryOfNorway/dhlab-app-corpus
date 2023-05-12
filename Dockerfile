FROM python:3.11-slim
EXPOSE 8501
WORKDIR /corpus.py
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run corpus.py  --server.baseUrlPath /korpus
