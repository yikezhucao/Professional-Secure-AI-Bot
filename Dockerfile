FROM python:3.12

WORKDIR /app

ARG OPENAI_API_KEY

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV http_proxy "http://172.17.0.1:7890"
ENV HTTP_PROXY "http://172.17.0.1:7890"
ENV https_proxy "http://172.17.0.1:7890"
ENV HTTPS_PROXY "http://172.17.0.1:7890"

COPY . /app

#RUN pip install -r requirements.txt --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install .

RUN python -m spacy download en_core_web_sm
# RUN proxychains python -m spacy download en_core_web_sm

# 拷贝模型到镜像中
#COPY ./spacy_models/en_core_web_sm /usr/local/lib/python3.12/site-packages/en_core_web_sm

# 注册 spacy 模型
#RUN python -m spacy link en_core_web_sm en

EXPOSE 5000

CMD ["secure_ai_bot"]
