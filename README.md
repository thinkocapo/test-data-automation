# Test Data Automation
Runs automted tests against Sentry demos on GCP, in order to generate errors and transactions to be sent to Sentry.io

## Components / Moving parts
- `conftest.py` -> Sauce Labs configuration (browsers) for frontend_tests
- `backend_tests/backend_test.py` -> Hits /handled, /unhandled/, + /checkout backend demo APIs

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
### Python, app, environment
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

### Metric Alerts for Low Traffic monitoring
This is so you can monitor it's running correctly, and get notified if the job stops running.
```
event.type:transaction
transaction:get_tools # the transaction you want to monitor
function:count() over a 5 minuets window

Critical Status
Below:2
```
The average transactions per 5-minute interval should be between 50 and 200, if you're monitoring it in a Metric Alert.

# Run: Continuously in VM (Compute Engine)
Use an isolated VM since it's constantly occupying +2 threads simultaneously
```
source .virtualenv/bin/activate
nohup ./script.sh &
```

How to stop it
```
ps fjx
kill -9 <PID of the bash process with script.sh>
```


## How to Verify Things are Are Working
#### WebVitals
Let your job run then Check LCP WebVital for one of your JS transactions:
![LCP1](img/lcp-1.png)

#### Trends
![Trends1](img/trends-1.png)

# GIF
TODO

## Troubleshooting
- Tests may fail intermittently due to instability of connections/selenium/etc. 
- Using more threads `-n` means more transactions, so less likely to dip below a Low Traffic threshold (metric alert)
- Front end apps (containers) must make requests to unique Back end apps, and not share the same back end apps, or this will skew transaction numbers in metric alerts
- Transaction volume comes from both `frontend_tests` that hit front end apps which then call their corresponding backends, as well as `backend_tests` which only hit the backend apps.
- Make sure your Metric Alerts are set the same for each project, and you're monitoring the right event type (transactions vs error)

# Setting up GCP cron job to trigger simulations
12/11/2020 Update - This is not actively being used. See Run instructions.

- `create_job.sh` -> creates GCP cron job which hits Travis requests APIs to trigger build
- `.travis.yml` -> runs automated tests / simulations

create_cron_job.sh -> GCP-cron job (runs every 20 min from midnight-6am) -> TravisCI (runs tests)

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