## Installation
Install docker and start all containers
```commandline
docker compose up -d
```

### Run Migrations
```commandline
./scripts/run_migrations.sh
```

### Populate DB
```commandline
./scripts/populate_db.sh
```


### Test application
http://localhost:8545/docs


## Developmemt Setup
Install the following.
1. Python 3.12.8
2. [Poetry](https://python-poetry.org/docs/#installation)

Run the following command to install project dependencies. Assuming you're in project root directory.
```commandline
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
