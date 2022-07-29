#!/usr/bin/env python3.9
import asyncio
from argparse import ArgumentParser as ArgumentParser
import configparser
import logging
from boto3 import Session as Session
import sys
from scramjet.streams import Stream


async def stdin_s3(stream):

    stream.write('Connect to stdin via API (si inst stdin <instance id>)')
    stream.write('and send your data s3')

    parser = ArgumentParser()
    parser.add_argument('-f', '--object_name', default='data001', required=False)
    parser.add_argument('-c', '--config', default='config.ini', required=False)
    parser.add_argument('-l', '--loglevel', default='INFO',
                        choices=['INFO', 'DEBUG', 'ERROR'])

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    logging.basicConfig(level=args.loglevel.upper())

    endpoint = config['aws']['endpoint_url']
    region = config['aws']['region']
    access_key_id = config['aws']['access_key_id']
    secret_access_key = config["aws"]["secret_access_key"]
    bucket = config['aws']['bucket']
    object_name = args.object_name

    session = Session()

    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        endpoint_url=endpoint,
        region_name=region
        )
    # get from stdin
    input = (await sys.stdin.read()).strip()

    stream.write("Bucket: {0} ObjectKey: {1}, stdin: {2}".format(bucket, object_name, input))

    req = s3_client.put_object(Body='{}'.format(input), Bucket=bucket, Key=args.object_name)
    stream.write(req)

    stream.write("Uploaded to S3 successfully")

    obj = s3_client.get_object(Bucket=bucket, Key=object_name)
    body = obj['Body'].read().decode('utf-8')

    stream.write("Read from S3 Bucket: {0} ObjectKey: {1}, Body: {2}".format(bucket, object_name, body))


async def run(context, input):

    # return Stream.read_from(input).map(stdin_s3)
    stream = Stream()
    asyncio.create_task(stdin_s3(stream))
    return stream.map(lambda s: s+'\n')
