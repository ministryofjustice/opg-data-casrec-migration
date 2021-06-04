FROM opg_casrec_migration_base_image:latest
RUN apt-get install -y postgresql-client curl unzip
ENV TF_VERSION=0.14.11
ENV TF_SHA256SUM=171ef5a4691b6f86eab524feaf9a52d5221c875478bd63dd7e55fef3939f7fd4
RUN curl -sfSO https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip
RUN echo "${TF_SHA256SUM} terraform_${TF_VERSION}_linux_amd64.zip" > SHA256SUMS
RUN sha256sum -c --status SHA256SUMS
RUN unzip terraform_${TF_VERSION}_linux_amd64.zip -d /bin

COPY run_ecs_task.py /run_ecs_task.py
COPY run_ecs_task.sh /run_ecs_task.sh
RUN chmod 755 run_ecs_task.sh && chmod 755 run_ecs_task.py
CMD ["bash", "./run_ecs_task.sh"]
