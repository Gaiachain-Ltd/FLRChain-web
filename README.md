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
2. Run ``` docker-compose stop ``` (we have to stop node to run catchup).
3. Run ``` docker-compose run algorand bash ```.
4. Run in Algorand bash ```./goal node start -d data```.
5. Run in Algorand bash ```./update.sh -d data```.
6. Obtain catchup point from https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup. For TestNet: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/testnet/latest.catchpoint.
7. Run in Algorand bash ```./goal node catchup <paste catchup point here!> -d data```.
8. Run in Algorand bash ```./goal node status -d data -w 1000``` and wait till you see text ```Sync Time: 0.0s```.
9.  Run in Algorand bash ``` cp data/config.json.example data/config.json ```.
10. Edit ```"EnableDeveloperAPI": false,``` to ```"EnableDeveloperAPI": true,``` in data/config.json.
11. Add to backend/.env token from data/algod.token like ```ALGO_API_TOKEN=<token>```.
12. Run in Algorand bash ```exit```.

## IV. Setup main account (test-net):
1. Create superuser ``` docker-compose run backend python manage.py createsuperuser ```.
2. Run ``` docker-compose run backend python manage.py generateaddress ```
3. You will see address and private key in output, please save it.
4. Go to https://dispenser.testnet.aws.algodev.network/ and paste your address there and click "Dispense".
5. Run in seprate terminal ``` docker-compose up algorand ```.
6. Run ``` docker-compose run backend python manage.py usdcoptin <ADDRESS> <PRIVATE_KEY> ```.
7. Go again to https://dispenser.testnet.aws.algodev.network/ and check "100 USDC" and paste your address there and click "Dispense".
8. Go to django admin panel and add new Accounts/Account. Paste address, private key, set type on "Main account" and set user as superuser.

## V. Run test-net live tests:
1. Copy backend/accounts/fixtures/example.main_account.json backend/accounts/fixtures/main_account.json .
2. Paste your address and private key from previous section into main_account.json.
3. You can track your tests here ```https://testnet.algoexplorer.io/address/<YOUR ADDRESS>```