FROM continuumio/miniconda3

# Pull the environment name out of the conda.yaml
COPY conda.yaml conda.yaml

RUN conda env create -f conda.yaml -n env
RUN conda init bash
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

