# NTD Data Copier
This repository contains code to obtain and update data from the National Transit Database via the API. The NTD does not allow public access for queries, so this repository will let you create a local copy which is synced to the NTD.

## Setup
To use this repository, you must already have access to a PostgreSQL database where you intend to store the NTD data. Next, create a `.env` file in the root repository directory using the template file `env_template.txt` to list your credentials and system specifications.

## Copying Data
Run the Python script `update_ntd_data.py` to create a local copy of the NTD in the database specified during setup. Re-run as needed to keep the data in sync.
