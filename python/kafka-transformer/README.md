# Sequence sending data to any Kafka topic

In this sample you can send data to Kafka topic from input.

If you are looking for more advanced demo of usage, please check [README](../../guides/kafka-setup/README.md)

First, build kafka-transformer sample

```bash
cd kafka-transformer
npm run build
```

Now you can run STH and deploy Sequence

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

On the second terminal

```bash
si seq deploy kafka-transformer/dist --args [{\"topic\":\"TOPIC\"},{\"server\":\"0.0.0.0:29092\"}]
```

Please note, that you need to deploy transformer sample with two args. One is topic, which is Kafka Topic name, to which you want to forward data. Second argument is address of your Kafka.

Last step is to start sending some data to transformer Sequence, which send it to Kafka topic.

```bash
si inst input -
```

Type anything you want to blinking terminal, you should be able to see forwarded data directly in Kafka on specific topic. You could use command below with your Kafka to check specific TOPIC.

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic TOPIC --from-beginning
```
