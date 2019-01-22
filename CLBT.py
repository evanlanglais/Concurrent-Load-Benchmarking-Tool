import argparse
import requests
import yaml
import logging
import sys

log = logging.getLogger("Concurrent Load Benchmarking Tool")


parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoints", type=str, help="A YAML file describing url endpoints")
parser.add_argument("-l", "--logging", default="DEBUG", help="Set console logging level")
args = parser.parse_args()

log.setLevel(logging.DEBUG)
stdhandler = logging.StreamHandler(sys.stdout)
stdhandler.setLevel(logging.getLevelName(args.logging))
log.addHandler(stdhandler)
log.debug("Parsed Args")

try:
    endpoints = yaml.save_load(args.endpoints)
    log.debug("Loaded endpoint file")
except:
    log.error("Error loading endpoint file")
    log.debug("Quitting")
    sys.exit()