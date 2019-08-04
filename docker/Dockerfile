FROM centos:7

ARG python_version

WORKDIR /install

COPY ./install_mod_wsgi_apache.sh /install

RUN /install/install_mod_wsgi_apache.sh ${python_version}