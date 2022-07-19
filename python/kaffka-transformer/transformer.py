from kafka import KafkaProducer
from scramjet.streams import Stream

def truncate(data):
    run.producer.send(run.TOPIC, value=str.encode(data.strip()))

async def run(context, input, *args):
    run.TOPIC = args[0].get('topic')
    run.BOOTSTRAP_SERVERS=args[1].get('server')
    run.producer = KafkaProducer(bootstrap_servers=run.BOOTSTRAP_SERVERS)
    return (
        Stream
            .read_from(input, max_parallel=1)
            .each(truncate)
    )
