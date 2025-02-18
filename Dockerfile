FROM bentoml/model-server:0.11.0-py37
MAINTAINER ersilia

RUN pip install rdkit==2022.9.5
RUN pip install numpy==1.21.6
RUN pip install pandas==1.1.5
RUN pip install torch torchaudio torchvision
RUN pip install tqdm==4.65
RUN pip install typing-extensions==4.5.0
RUN pip install typed-argument-parser==1.8.0
RUN pip install tensorboardX==2.6
RUN pip install scikit-learn
RUN pip install hyperopt==0.2.7
RUN conda install -c conda-forge xorg-libxrender xorg-libxtst

WORKDIR /repo
COPY . /repoFROM ersiliaos/base-v2:latest as build
ARG MODEL=eos3ev6
ENV MODEL=$MODEL
RUN ersilia -v fetch $MODEL --from_github
# Install conda pack so we can create a standalone environment from
# the model's conda environment
RUN conda install -c conda-forge -y conda-pack
RUN conda-pack -n $MODEL -o /tmp/env.tar && \
    mkdir /$MODEL && cd /$MODEL && tar xf /tmp/env.tar && \
    rm /tmp/env.tar
RUN /$MODEL/bin/conda-unpack

# Now we can create a new image that only contains
# the ersilia environment, the model environment, 
# and the model itself (as a bentoml bundle)

FROM python:3.7-slim-buster
WORKDIR /root
ARG MODEL=eos3ev6
ENV MODEL=$MODEL

# The following lines ensure that ersilia environment is directly in the path
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

# We install nginx here directly instead of the base image
RUN apt-get update && apt-get install nginx -y

# Copy the model env and ersilia env from the build image
COPY --from=build /$MODEL /$MODEL
COPY --from=build /venv /venv

# Retain the bundled model bento from the build stage
COPY --from=build /root/eos /root/eos
# Copy bentoml artifacts so it doesn't complain about model bento not being found
COPY --from=build /root/bentoml /root/bentoml

COPY --from=build /root/docker-entrypoint.sh docker-entrypoint.sh
COPY --from=build /root/nginx.conf /etc/nginx/sites-available/default

# Writing this script here because the Dockerfile gets copied to the model directory
# and the model directory is not known until the build stage. Either we copy this script
# within the build context or we write it here.
RUN echo -e "#!/bin/bash\nset -eux\n\
cd ~/bentoml/repository/$MODEL/*/$MODEL/artifacts/\n\
if [ -f framework/run.sh ]; then\n\
  sed -i -n 's/\/usr\/bin\/conda\/envs//p' framework/run.sh\n\
fi" > patch_python_path.sh && \
chmod +x patch_python_path.sh && \
./patch_python_path.sh

RUN chmod + docker-entrypoint.sh
EXPOSE 80
ENTRYPOINT [ "sh", "docker-entrypoint.sh"]
