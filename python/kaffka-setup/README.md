# Sequences fetching and sending data from any Kafka server

Easy example of usage Kaffka with Scramjet platform. As the part of this PR, three different directories are created for organizational purposes. You need also 3 different terminals to check the whole.

On first terminal:

setup kaffka in docker container

```bash
cd kaffka-setup
docker-compose up -d
```

create 'scramjet' topic

```bash
docker-compose exec kafka kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic scramjet
```

run watcher for 'scramjet' topic, you will see here logs directly from kaffka

```bash
docker-compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic scramjet --from-beginning
```

On second terminal run STH

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

On last terminal you need to make few things. First you need to build our two samples. You can run command visible below in main directory of platform-samples project to build all samples, or you can run it directly from the kaffka-transformer and kaffka-consumer directories.

```bash
npm run build
```

Once you've built these packages, you need to run consumer Sequence first. Please note that we are passing two arguments to Sequence, topic name and server name.

```bash
si seq deploy kaffka-consumer/dist --args [{\"topic\":\"scramjet\"},{\"server\":\"0.0.0.0:29092\"}]
```

Now you can deploy transform Sequence, with exactly same arguments:

```bash
si seq deploy kaffka-transformer/dist --args [{\"topic\":\"scramjet\"},{\"server\":\"0.0.0.0:29092\"}]
```

You should be able to list both instances with command:

```bash
si inst ls`
```

Last step is to start sending some data to transformer Sequence, which send it to Kaffka topic.

```bash
si inst input -
```

Type anything you want to blinking terminal, you should then see same data in first terminal, which shows logs from kaffka directly, but also you should be able to see information on STH terminal. It should look similar to:

```bash
Topic name=scramjet, Message=b'test message'
```
