# First time:

## I. Requirements:
1. Download and setup ```docker```.
2. Download and setup ```docker-compose```.

## II. Instructions for frontend/backend:
1. Copy backend/sample.env to backend/.env ``` cp backend/sample.env backend/.env ```.
2. Put correct data into backend/.env if you need.
3. Copy frontend/sample.env to frontend/.env ``` cp frontend/sample.env frontend/.env ```.
3. Put correct data into frontend/.env if you need.
4. Run ``` docker-compose build ```.
5. Run ``` docker-compose run backend python manage.py migrate ```.
6. Run ``` docker-compose run backend python manage.py collectstatic ```.
5. Run ``` docker-compose up -V ```.

## III. Instructions Algorand node:
1. Make sure you have done everything from instructions above.
2. Run ``` docker-compose run algorand bash ```.
3. Run in Algorand bash ```./goal node start -d data```.
4. Obtain catchup point from https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup. For TestNet: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint.
5. Run in Algorand bash ```./goal node catchup <paste catchup point here!> -d data```.
6. Run in Algorand bash ```./goal node status -d data -w 1000``` and wait till you see text ```Sync Time: 0.0s```.
7. Run in Algorand bash ```exit```.