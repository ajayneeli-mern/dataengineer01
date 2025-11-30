FROM apache/airflow:2.7.3-python3.11

USER root

# Install Terraform
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_linux_amd64.zip && \
    unzip terraform_1.6.6_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.6.6_linux_amd64.zip && \
    apt-get clean



USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean
USER root
RUN mkdir -p /opt/airflow/project_root/data && \
    mkdir -p /opt/airflow/project_root/my_dbt/seeds && \
    chown -R airflow:0 /opt/airflow/project_root

USER airflow
# Install any additional Python packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
