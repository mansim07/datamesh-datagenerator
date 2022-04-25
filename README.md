# data-generator
A data generator library for generating data for the retail banking use case using the Faker library

## Generating Customer Data 
This will generate the customer identifiers and customer_credit_card identifiers data and upload it to GCS. 

Step1: Clone this repo 

```
git clone https://github.com/mansim07/datamesh-datagenerator
```

Step2: Use Python 3

```
pip install faker
pip install google-cloud-storage
pip install numpy
pip install faker_credit_score
```

Step3: 

```
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credential.json
```

Step4: Execute the script 

```
cd customer_data

python3 create_customers.py num_of_customers seed_value json-profile-file gcp-project-name gcs-bucketname
```

e.g. 
python3 create_customers.py 10 430 ../profiles/main_config.json customers-323 bankofmars_retail_banking_customers