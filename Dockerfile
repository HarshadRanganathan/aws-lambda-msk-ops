FROM public.ecr.aws/lambda/python:3.11

#
# Versions
#
ARG KAFKA_VERSION=3.6.1

# Install Kafka Pre-reqs
RUN yum -y install java-11 wget tar;  yum clean all
RUN yum -y update -y && yum clean all && \
rm -rf /var/cache/yum

# Install Kafka
RUN wget https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_2.12-${KAFKA_VERSION}.tgz
RUN tar -xzf kafka_2.12-${KAFKA_VERSION}.tgz

# Cleanup
RUN rm kafka_2.12-${KAFKA_VERSION}.tgz

#
# Copy Artifacts
#
COPY code/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY code/kafka.properties ${LAMBDA_TASK_ROOT}

# Run handler
CMD ["lambda_function.lambda_handler"]
