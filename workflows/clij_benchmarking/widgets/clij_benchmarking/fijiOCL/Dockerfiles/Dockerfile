FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y install default-jdk tar wget curl \
    nvidia-driver-510-server ocl-icd-opencl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN wget -c https://downloads.imagej.net/fiji/archive/20201104-1356/fiji-linux64.tar.gz \
    -O - | tar -xz -C /usr/local/bin/
ENV PATH $PATH:/usr/local/bin/Fiji.app
ADD startfiji.sh /usr/local/bin/startfiji.sh
RUN ImageJ-linux64 --update add-update-site clij https://sites.imagej.net/clij && \ 
    ImageJ-linux64 --update add-update-site clij2 https://sites.imagej.net/clij2 && \
    ImageJ-linux64 --update update
