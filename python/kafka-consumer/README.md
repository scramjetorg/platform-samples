# Sequence fetching data from any Kafka topic

In this sample you can retrieve data from Kafka topic and show the result on 'output'.

___

If you are looking for more advanced demo of usage, please check [README](../../guides/kafka-setup/README.md)

## Running

> ❗ Remember to [setup transform-hub locally](https://docs.scramjet.org/transform-hub/installation) or use the [platform's environment](https://docs.scramjet.org/platform/get-started/) for the sequence deployment.

First, build kafka-consumer sample

```bash
# go to 'kafka-consumer' directory
cd python/kafka-consumer

# build
npm run build
```

If you run this sample on Self Hosted Hub, please start it with process adapter option:

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

**The second terminal**

```bash
si seq deploy kafka-consumer/dist --args [{\"topic\":\"TOPIC\"},{\"server\":\"0.0.0.0:29092\"}]
```

Please note, that you need to deploy consumer sample with two args. One is topic, which is Kafka Topic name, from which you want to consume data. Second argument is address of your Kafka.

If you have data on specified topic, you should be able to see information on STH terminal. It should look similar to:

```bash
Topic name=TOPIC, Message=b'test message'
```
