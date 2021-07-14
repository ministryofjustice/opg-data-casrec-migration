FROM opg_casrec_migration_base_image:latest
RUN apt-get install -y postgresql-client
COPY case_details_to_s3.py /case_details_to_s3.py
CMD ["echo", "NO_OP"]
