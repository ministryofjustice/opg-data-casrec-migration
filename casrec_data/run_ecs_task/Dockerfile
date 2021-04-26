FROM opg_casrec_migration_base_image:latest
RUN apt-get install -y postgresql-client
COPY run_ecs_task.py /run_ecs_task.py
CMD ["echo", "NO_OP"]
