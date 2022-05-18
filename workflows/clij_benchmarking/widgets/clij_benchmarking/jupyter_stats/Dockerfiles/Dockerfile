FROM biodepot/jupyter:5.6.0__ubuntu-18.04__081318
RUN apt-get update && apt-get -y install firefox python3-matplotlib python3-pandas python3-numpy python3-scipy \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*