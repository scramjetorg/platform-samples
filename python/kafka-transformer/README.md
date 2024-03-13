# Sequence sending data to any Kafka topic

In this sample you can send data to Kafka topic from input.

___

If you are looking for more advanced demo of usage, please check [README](../../guides/kafka-setup/README.md)

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

Open two terminals and run the following commands:

**The first terminal:**

First, build kafka-transformer sample

```bash
# go to 'kafka-transformer' directory
cd python/kafka-transformer

# build
npm run build
```

If you run this sample on Self Hosted Hub, please start it with process adapter option:

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

**The second terminal**

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
