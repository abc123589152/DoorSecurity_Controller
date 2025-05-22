FROM ubuntu_python_311_5:v1

RUN mkdir /controller_input

WORKDIR /controller_input

COPY requirementes.txt /controller_input/requirementes.txt

COPY controller_input_base.py /controller_input/controller_input_base.py

COPY module/ /controller_input/module

RUN pip install -r requirementes.txt

CMD ["tail", "-f", "/dev/null"]