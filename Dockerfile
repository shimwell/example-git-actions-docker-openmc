
FROM ubuntu:18.04

# Python and OpenMC installation

RUN apt-get --yes update && apt-get --yes upgrade

RUN apt-get -y install locales
RUN locale-gen en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Install Packages Required
RUN apt-get --yes update && apt-get --yes upgrade
RUN apt-get --yes install gfortran 
RUN apt-get --yes install g++ 
RUN apt-get --yes install cmake 
RUN apt-get --yes install libhdf5-dev 
RUN apt-get --yes install git
RUN apt-get update

RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-setuptools
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y ipython3
RUN apt-get update
RUN apt-get install -y python3-tk

#Install unzip
RUN apt-get update
RUN apt-get install -y unzip

#Install Packages Optional
RUN apt-get --yes update
RUN apt-get --yes install imagemagick
RUN apt-get --yes install hdf5-tools
RUN apt-get --yes install paraview
RUN apt-get --yes install eog
RUN apt-get --yes install wget
RUN apt-get --yes install firefox
RUN apt-get --yes install dpkg
RUN apt-get --yes install libxkbfile1

#Install Packages Optional for distributed memory parallel simulations
RUN apt install --yes mpich libmpich-dev
RUN apt install --yes openmpi-bin libopenmpi-dev

RUN apt-get --yes install libblas-dev 
# RUN apt-get --yes install libatlas-dev 
RUN apt-get --yes install liblapack-dev

# Clone and install NJOY2016
RUN git clone https://github.com/njoy/NJOY2016 /opt/NJOY2016 && \
    cd /opt/NJOY2016 && \
    mkdir build && cd build && \
    cmake -Dstatic=on .. && make 2>/dev/null && make install

RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3 /usr/bin/python


# installs OpenMc from source 
RUN cd opt && \
    git clone https://github.com/openmc-dev/openmc.git && \  
    cd openmc && \
    git checkout develop && \
    mkdir build && cd build && \
    cmake .. && \
#    cmake -Ddebug=on .. && \
    make && \
    make install

RUN cd /opt/openmc && pip3 install .

RUN git clone https://github.com/openmc-dev/data.git

# run script that converts ACE data to hdf5 data
RUN python3 data/convert_nndc71.py --cleanup

ENV OPENMC_CROSS_SECTIONS=/nndc-b7.1-hdf5/cross_sections.xml






# make sure that pytest is installed
# we'll need it to run the tests!
RUN pip install pytest

# Copy over the source code
COPY minimal_openmc_simulations minimal_openmc_simulations/

# Copy over the test folder
COPY tests tests/

CMD ["/bin/bash"]
