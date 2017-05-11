FROM gsiupm/senpy:0.8.7-python3.5

RUN apt-get update && apt-get install -q -y unzip make g++ wget git git-core mercurial bzip2 autotools-dev automake libtool zlib1g-dev libbz2-dev libboost-all-dev libxmlrpc-core-c3-dev libxmlrpc-c++8-dev build-essential pkg-config python-dev cmake libcmph-dev libcmph-tools libcmph0 libgoogle-perftools-dev liblzma-dev
RUN git clone https://github.com/moses-smt/mosesdecoder.git
RUN mkdir -p /home/mosesdecoder
WORKDIR mosesdecoder/
RUN ./bjam --prefix=/home/mosesdecoder --install-scripts --with-cmph=/usr/include/cmph --with-xmlrpc-c -j8
RUN rm -rf mosesdecoder/
WORKDIR /
RUN wget http://server1.nlp.insight-centre.org/docker/translate.perl
RUN chmod +x translate.perl

COPY logo-Insight.png /usr/local/lib/python3.5/site-packages/senpy/static/img/gsi.png
RUN perl -i -pe s^http://www.gsi.dit.upm.es^https://nuig.insight-centre.org/unlp/^g /usr/local/lib/python3.5/site-packages/senpy/templates/index.html
RUN perl -i -pe 's^https://nuig.insight-centre.org/unlp/" target="_blank"><img id="mixedemotions-logo^http://mixedemotions-project.eu/" target="_blank"><img id="mixedemotions-logo^g' /usr/local/lib/python3.5/site-packages/senpy/templates/index.html
