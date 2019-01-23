import argparse
import requests
import yaml
import logging
import sys
import random
import time
import threading
import matplotlib.pyplot as plt

version = "1.0"

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--routes", type=str, help="A YAML file describing url endpoints")
parser.add_argument("-l", "--logging", default="DEBUG", help="Set console logging level")
parser.add_argument("-g", "--graph", help="Graph results flag", action='store_true')
parser.add_argument("-min", type=int, default=1)
parser.add_argument("-max", type=int, default=25)
parser.add_argument("-t", "--trials", type=int, default=4)
parser.add_argument("-q", "--queries", type=int, default=10)
args = parser.parse_args()

log = logging.getLogger("Concurrent Load Benchmarking Tool")
log.setLevel(logging.DEBUG)
stdhandler = logging.StreamHandler(sys.stdout)
stdhandler.setLevel(logging.getLevelName(args.logging))
log.addHandler(stdhandler)

log.info("Concurrent Load Benchmarking Tool v%s" % (version))

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

total_elapsed = [0.0] * (args.max - args.min + 1)
total_points = [0] * (args.max - args.min + 1)
total_failed = [0] * (args.max - args.min + 1)

trial_elapsed = 0.0
trial_points = 0
trial_failed = 0
trial_lock = threading.Lock()

def thread_process():
    thread_elapsed = 0.0
    thread_runs = 0
    thread_failures = 0
    global trial_elapsed, trial_points, trial_failed
    s = requests.Session()
    for q in range(args.queries + 1):
        req = getThreadRequest(routes)
        prep = req.prepare()
        start = time.perf_counter()
        response = s.send(prep)
        elapsed = time.perf_counter() - start
        if(response.status_code == 200):
            thread_elapsed += elapsed
            thread_runs += 1
        else:
            thread_failures += 1
    with trial_lock:
        trial_elapsed += thread_elapsed
        trial_points += thread_runs
        trial_failed += thread_failures

log.info("Starting Tests for %s" % (routes['site']))

threads = []
for workers in range(args.min, args.max + 1):
    log.info("Starting testing for %d concurrent users" % (workers))
    for trial in range(1, args.trials + 1):
        log.info("Starting Trial %d" % trial)
        for i in range(workers):
            t = threading.Thread(target=thread_process)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        threads = []
    total_elapsed[workers - args.min] += trial_elapsed
    total_points[workers - args.min] += trial_points
    total_failed[workers - args.min] += trial_failed
    trial_elapsed = 0.0
    trial_points = 0
    trial_failed = 0

avg_rt = [x/y for x, y in zip(total_elapsed, total_points)]
log.info(avg_rt)
log.info(total_failed)

if args.graph:
    plt.figure(1)
    plt.subplot(211)
    plt.plot(avg_rt)
    plt.title("Benchmark Results For %s" % (routes['site']))
    plt.ylabel("Average Response Time (s)")
    plt.subplot(212)
    plt.plot(total_failed)
    plt.ylabel("Failures")
    plt.ylim(0, 100)
    plt.show()