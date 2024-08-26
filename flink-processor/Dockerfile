# Use an official OpenJDK runtime as a parent image
FROM openjdk:8u151-jdk-alpine3.7

# Install bash and other necessary packages
RUN apk add --no-cache bash libc6-compat

# Copy resources
WORKDIR /
COPY wait-for-it.sh wait-for-it.sh

COPY target/flink-processor-1.0-jar-with-dependencies.jar flink-processor.jar


# Wait for Zookeeper and Kafka to be available and run application
CMD ./wait-for-it.sh -s -t 30 $ZOOKEEPER_SERVER -- ./wait-for-it.sh -s -t 30 $KAFKA_SERVER -- java -Xmx512m -jar flink-processor.jar