import argparse
import requests
import yaml
import logging
import sys
import random
import time

version = 1.0

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--routes", type=str, help="A YAML file describing url endpoints")
parser.add_argument("-l", "--logging", default="DEBUG", help="Set console logging level")
parser.add_argument("-g", "--graph", default=False, help="True/False should we graph results", type=bool)
parser.add_argument("-min", type=int, default=1)
parser.add_argument("-max", type=int, default=20)
parser.add_argument("-t", "--trials", type=int, default=4)
parser.add_argument("-q", "--queries", type=int, default=10)
args = parser.parse_args()

log = logging.getLogger("Concurrent Load Benchmarking Tool")
log.setLevel(logging.DEBUG)
stdhandler = logging.StreamHandler(sys.stdout)
stdhandler.setLevel(logging.getLevelName(args.logging))
log.addHandler(stdhandler)

log.info("Concurrent Load Benchmarking Tool v%f" % (version))

log.debug("Parsed Args")

try:
    with open(args.routes, 'r') as f:
        routes = yaml.safe_load(f)
    log.debug("Loaded routing file")
except:
    log.error("Error loading routing file")
    log.debug("Quitting")
    sys.exit()

def getThreadRequest(routes):
    sel = random.randrange(routes['weight-total'])
    total = 0
    for endpoint in routes['endpoints']:
        if(sel >= total and sel <= total + endpoint['weight']):
            filled_params = {}
            if 'variables' in endpoint:
                for var in endpoint['variables']:
                    val = random.randrange(len(var['values']))
                    filled_params[var['key']] = var['values'][val]
            return requests.Request(endpoint['type'], routes['base-url'] + endpoint['url'], params=filled_params)
        else:
            total += endpoint['weight']

def thread_process(i):
    total_elapsed = 0.0
    total_runs = 0
    failed_runs = 0
    s = requests.Session()
    for q in range(args.queries):
        req = getThreadRequest(routes)
        prep = req.prepare()
        start = time.process_time()
        response = s.send(prep)
        elapsed = time.process_time() - start
        total_elapsed += elapsed
        total_runs += 1
        if(response.status_code != 200):
            failed_runs += 1
    log.info("Thread %d finished running %d queries with %d failures" % (i, total_runs, failed_runs))

log.info("Starting Tests for %s" % (routes['site']))

thread_process(1)