# Sequences fetching and sending data from any Kafka server

A simple example showcasing Kafka usage with Scramjet platform. 
___
## Prerequisites
As a part of this PR, 3 different directories are created for organizational purposes. 

You will need 3 different terminal windows.

## Running

**On the first terminal:**

- setup kafka in a docker container

```bash
cd guides/kafka-setup
docker-compose up -d
```

- create '*scramjet*' topic

```bash
docker-compose exec kafka kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic scramjet
```

- run watcher for 'scramjet' topic, you will see here logs directly from kafka

```bash
docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic scramjet --from-beginning
```

**On the second terminal:**

- run STH
```bash
DEVELOPMENT=1 sth --runtime-adapter=process
# DEVELOPMENT=1   will make STH output all logs
# --runtime-adapter=process   will make STH run without docker
```

**On the third terminal:**

- build both of the samples. You can run the command below in the root directory of platform-samples which will build all samples, or you can run it separately inside **kafka-transformer** and **kafka-consumer** directories.

```bash
npm run build
```

- run **consumer Sequence**
 > 💡 You need to pass 2 arguments to the Sequence: ***topic name*** and ***server name***.

```bash
si seq deploy python/kafka-consumer/dist --args [{\"topic\":\"scramjet\"},{\"server\":\"0.0.0.0:29092\"}]
```

- run **transform Sequence** with exactly the same arguments

```bash
si seq deploy python/kafka-transformer/dist --args [{\"topic\":\"scramjet\"},{\"server\":\"0.0.0.0:29092\"}]
```

- send some data to the **transformer Sequence**, which will send it to the Kafka topic

```bash
si inst input -

# Now type anything into the terminal
```

- you should see the same output on both the first terminal (which shows logs from kafka) and the STH terminal. It should look like this

```bash
Topic name=scramjet, Message=b'test message'
```
