# Concurrent Load Benchmarking Tool (CLBT)
A benchmarking tool to test web and RESTful services' readiness for concurrent loads.


## Product Motivation
When developing web services there are many different decisions made in order to ensure that performance of the service is optimal. Of course low latency is of top priority, however a service's specific configuration, technologies, and infrustructure can impact how that latency scales with increasing web-traffic.

The Concurrent Load Benchmarking Tool (CLBT) attempts to simulate, measure, and graph the average latency experienced by any given user using your webservice with a specific number of concurrent users doing the same. It is meant to act as a standardized benchmark when developing the webservice to compare measure the performance delta of using different frameworks, cloud services, caching systems, etc.

## Requirements
1. Python 3
2. Pip
3. Pipenv

## Installation
1. Clone Repository
2. Install all packages using `pipenv install`

## Usage
To use the CLBT for your own webservice you must:

### Create Webservice Routing File
The first step in using the CLBT to test your webservice is to create the webservice routing file. The routing file is written in YAML formatting and has a specific universal structure in order for the tool to accurately and consistently test any given webservice.