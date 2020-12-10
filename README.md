# Test Data Automation
Runs automted tests against Sentry demos on GCP, in order to generate errors and transactions to be sent to Sentry.io

## Components / Moving parts
- `create_job.sh` -> creates GCP cron job which hits Travis requests APIs to trigger build
- `.travis.yml` -> runs automated tests / simulations
- `conftest.py` -> Sauce Labs configuration (browsers) for frontend_tests
- `backend_tests/backend_test.py` -> Hits /handled, /unhandled/, + /checkout backend demo APIs

create_cron_job.sh -> GCP-cron job (runs every 20 min from midnight-6am) -> TravisCI (runs tests)

# Tests

## FrontEnd / Selenium (`frontend_tests` directory)
Pulls up Sentry frontend in various browsers in parallel via selenium scripts.
Test case will add items to cart and then click checkout

```
pip install -r requirements.txt
py.test -s -n 2 frontend_tests
```

`-n` is for number of threads

## Backend (`backend_tests` directory)
Hits /unhandled, /handled, + /checkout backend demo APIs
```
cd backend_tests
python backend_test.py
```
# Setup
Python2  
SAUCE_USERNAME  
SAUCE_ACCESS_KEY

If you get this error during pip install: `ERROR: Package 'setuptools' requires a different Python: 2.7.12 not in '>=3.5'` then run:
```
pip install -U pip
pip install setuptools==44.0.0

# and re-rerun:
pip install -r requirements.txt
```

Set your `DSN` in:
```
touch .env
```
This is so any errors occuring in conftest.py (the pytest and updates on selenium jobs) get reported.

# Setup: Setting up cron job to trigger simulations

We can trigger the travis builds on a schedule via Google Cloud Scheduler cron jobs.

To register:
```
./create_cron_job.sh
```

Docs:
- https://cloud.google.com/sdk/gcloud/reference/scheduler/jobs/create/
- https://docs.travis-ci.com/user/triggering-builds/

Sentry docs:
- https://docs.sentry.io/performance/distributed-tracing/
- https://docs.sentry.io/performance/performance-metrics/

# GIF
TODO

# To run "continuously" in VM
Use an isolated VM since it's constantly occupying +2 threads simultaneously
```
source .virtualenv/bin/activate
nohup ./script.sh &
```

How to stop it
```
ps fjx
kill -9 <PID of the script.sh>
```

## How to Verify Things are Are Working
#### WebVitals
Let your job run then Check LCP WebVital for one of your JS transactions:
![LCP1](img/lcp-1.png)

#### Trends
![Trends1](img/trends-1.png)

## Troubleshooting
- Tests may fail intermittently due to instability of connections/selenium/etc. 
- Using more threads `-n` means more transactions, so less likely to dip below a Low Traffic threshold (metric alert)