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
    
USER airflow
# Install dbt-core + dbt-mysql plugin
RUN pip install --no-cache-dir \
    dbt-core==1.7.19 \
    dbt-mysql==1.7.0

# Install any additional Python packages
RUN pip install --no-cache-dir apache-airflow-providers-docker
