FROM ubuntu_python_311_5:v1

RUN mkdir /controller_output

WORKDIR /controller_output

COPY requirementes.txt /controller_output/requirementes.txt

COPY controller_output_base.py /controller_output/controller_output_base.py

RUN pip install -r requirementes.txt

CMD ["tail", "-f", "/dev/null"]