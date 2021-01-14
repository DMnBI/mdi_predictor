FROM nvcr.io/nvidia/cuda:9.0-devel-ubuntu16.04
FROM nvcr.io/nvidia/tensorflow:20.12-tf1-py3

COPY ./code/stanza_down.py /workspace/code/stanza_down.py

RUN pip install stanza
RUN pip install openpyxl

WORKDIR /workspace

RUN python /workspace/code/stanza_down.py
