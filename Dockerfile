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

USER airflow

# Install additional Python packages if needed
RUN pip install --no-cache-dir apache-airflow-providers-docker