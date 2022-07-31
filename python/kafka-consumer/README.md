# Sequence fetching data from any Kafka topic

In this sample you can retrieve data from Kafka topic and show the result on 'output'.

If you are looking for more advanced demo of usage, please check [README](../kafka-setup/README.md)

First, build kafka-consumer sample

```bash
cd kafka-consumer
npm run build
```

Now you can run STH and deploy Sequence

```bash
DEVELOPMENT=1 sth --runtime-adapter=process
```

On the second terminal

```bash
si seq deploy kafka-consumer/dist --args [{\"topic\":\"TOPIC\"},{\"server\":\"0.0.0.0:29092\"}]
```

Please note, that you need to deploy consumer sample with two args. One is topic, which is Kafka Topic name, from which you want to consume data. Second argument is address of your Kafka.

If you have data on specified topic, you should be able to see information on STH terminal. It should look similar to:

```bash
Topic name=TOPIC, Message=b'test message'
```
