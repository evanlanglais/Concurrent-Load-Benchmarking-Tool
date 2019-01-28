# Concurrent Load Benchmarking Tool (CLBT)
A Python 3 Application to test RESTful API's and other webservices readiness for concurrent loads

## What is this?
When developing web services there are many different decisions made in order to ensure that performance of the service is optimal. Of course low latency is of top priority, however a service's specific configuration, technologies, and infrustructure can impact how that latency scales with increasing web-traffic.

The Concurrent Load Benchmarking Tool (CLBT) attempts to simulate, measure, and graph the average latency experienced by any given user using your webservice with a specific number of concurrent other users doing the same.

## Requirements
1. Python 3
2. Pip
3. Pyenv

## Installation
1. Clone Repository
2. Install all packages using pyenv
3. Create API routing file (discussed below)

## Test An API
Testing an API is not meant to have an apple's to apple's comparison between two different services. This tool of it are to measure and 
