FROM centos:7

ARG python_version

WORKDIR /install

COPY ./install_mod_wsgi_apache.sh /install

ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN /install/install_mod_wsgi_apache.sh ${python_version}

RUN rm -rf /install

CMD ["/usr/sbin/init"]

# https://serverfault.com/questions/824975/failed-to-get-d-bus-connection-operation-not-permitted
