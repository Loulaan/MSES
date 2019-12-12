FROM pytorch/pytorch:latest

RUN apt-get update && apt-get install -y git && apt-get install wget -y && apt install -y libsm6 libxext6 && apt-get install libxrender-dev -y && apt-get install libglib2.0-0 -y
RUN cd .. && git clone https://github.com/Loulaan/MSES && pip install cython

WORKDIR /MSES

RUN git pull
RUN pip install -U -r requirements.txt

COPY /weights /MSES/weights
COPY /newData /MSES/newData

EXPOSE 8888
EXPOSE 6006
EXPOSE 8080

CMD ["/bin/bash"]