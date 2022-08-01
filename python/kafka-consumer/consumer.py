from kafka import KafkaConsumer

async def run(context, input, *args):
    run.TOPIC = args[0].get('topic')
    run.BOOTSTRAP_SERVERS=args[1].get('server')
    consumer = KafkaConsumer(run.TOPIC, bootstrap_servers=run.BOOTSTRAP_SERVERS)
    for msg in consumer:
        print(f'Topic name={msg.topic}, Message={msg.value}')
