import sys
import datetime
import time
import numpy
import json
import random
import argparse
import boto3
import logging
from faker import Faker
from tzlocal import get_localzone

logging.basicConfig(filename='fake_log_gen.log', level=logging.INFO)

faker = Faker()
local_zone = get_localzone()

response = ["200","404","500","301"]
methods = ["GET","POST","DELETE","PUT"]
resources = ["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/order/detail?prodID="]
agents = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]


def put_to_stream(kinesis_cln, kinesis_stream_name, partition_key):
    fake_payload = generate_fake_payload()
    logging.info('Log payload %s', fake_payload)

    put_response = kinesis_cln.put_record(
        StreamName=kinesis_stream_name,
        Data=json.dumps(fake_payload),
        PartitionKey=partition_key)
    logging.info('Kinesis put response  %s', put_response)


def generate_fake_payload():
    host = faker.ipv4()
    curr_ts = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
    curr_lz = datetime.datetime.now(local_zone).strftime('%z')
    curr_ts_lz = '{} {}'.format(curr_ts, curr_lz)
    http_method = numpy.random.choice(methods, p=[0.6,0.2,0.1,0.1])
    http_resp = numpy.random.choice(response, p=[0.88,0.04,0.05,0.03])
    resp_bytes = int(random.gauss(4000,70))
    referer = faker.uri()
    user_agent = numpy.random.choice(agents, p=[0.3, 0.5, 0.1, 0.05, 0.05])()

    request_uri = '{} {}'.format(http_method, numpy.random.choice(resources))
    if request_uri.find("order") > 0:
        request_uri += str(random.randint(200, 8000))

    payload = {
        "host":host,
        "datetime": curr_ts_lz,
        "request": request_uri,
        "response": http_resp,
        "bytes": resp_bytes,
        "referer": referer,
        "useragent": user_agent
    }
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dummy Apache Log Generator")
    parser.add_argument("--stream", "-k", dest='stream_name', help="Kinesis Stream name to publish the logs",
                        default="apache-log-stream")
    parser.add_argument("--region", "-r", dest='region_name', help="Kinesis Stream Region",
                        default="us-west-1")
    parser.add_argument("--num", "-n", dest='num_lines', help="Number of lines to generate (0 for infinite)", type=int,
                        default=1)
    parser.add_argument("--sleep", "-s", dest='sleep_secs', help="Sleep between lines (in seconds)", default=0.0, type=float)

    args = parser.parse_args()
    num_lines = args.num_lines

    kinesis_client = boto3.client('kinesis', region_name=args.region_name)

    while (num_lines > 0):
        put_to_stream(kinesis_client, args.stream_name, 'aa')
        num_lines = num_lines - 1

        if args.sleep:
            time.sleep(args.sleep_secs)
