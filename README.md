# data-generator
A data generator library for generating data for the retail banking use case using the Faker library

## Generating Data
This module generates the below data, uploads it to GCS bucket and loads into a bq native table using bq load.

1. Customer data 
2. Customer to credit card mapping data 
3. Merchant data 
4. Credit Card transaction data

Apart from generating master data, the repo has a list of reference data that will be uploaded to GCS and loaded to BQ tables as well 
1. Merchant MCC codes 
2. Credit card reference data: 
    2.1. Card read type

    2.2  Card type facts

    2.3  Currency 

    2.4. Event types

    2.5. Origination Code

    2.6. Payment methods

    2.7. Signature 

    2.8. Swiped code

    2.9. Trans type
    

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

Step4: Change the inputs in the file 

    #date value for gcs path 
    date_partition=YYYY-MM-DD   #specified format only
    local_data_dir="local directory path for data" # e.g. /tmp/data

    #Customer Inputs
    customer_project=name-of-customer-project
    customer_bucket=name-of-customer-gcs-bucket
    customer_bq_table=customer_datasetname.customer_tablename
    cc_customer_map_bq_table=cc_customer_mapping_dataset.cc_customer_mapping_table
    customer_seed=1 #seed value 
    num_of_customers=10 #number off customer to generate
    profile_name="./profiles/main_config.json" #name of the profile
    customer_hive_parent="customers_data"
    cc_customer_parent="cc_customers_data"
    customer_file=customer.csv
    cc_customer_file=cc_customer.csv
    cc_merchant_file=cc_merchant_info_for_trans.csv
    customer_gcs_file="${customer_hive_parent}/dt=${date_partition}/${customer_file}"
    cc_customer_map_gcs_file="${cc_customer_parent}/dt=${date_partition}/${cc_customer_file}"

    #Merchant Inputs
    merchant_project=name-of-merchant-project
    merchant_bucket=name-of-merchant-gcs-bucket
    merchant_seed=1
    num_merchants=1000
    cc_merchant_data="merchants_data"
    ref_data_local_path="./merchant_data/data/ref_data"
    mcc_file_name="mcc_codes.csv"
    merchant_filename="merchants.csv"
    merchant_gcs_filename="${cc_merchant_data}/date=${date_partition}/${merchant_filename}"
    mcc_gcs_filename="mcc_codes/date=${date_partition}/${mcc_file_name}"
    #make sure "cc_merchant_file" is set
    merchant_bq_table=name-of-merchant-table
    mcc_bq_table="merchants_reference_data.mcc_code"


    #Credit Card Transactions Inputs
    credit_card_project=name-of-credit-card-project
    credit_card_bucket=name-of-credit-card-gcs-bucket
    cc_ref_bq_dataset="lookup_data"
    cc_hive_parent="auth_data"
    num_of_trans_per_cust=3
    cc_trans_seed=1
    trans_filename=trans_data.csv
    cc_auth_gcs_path="${cc_hive_parent}/date=${date_partition}/${trans_filename}"
    start_date=2022-01-01
    end_date=2022-01-02
    trans_ref_data="./transaction_data/data/ref_data"
    auth_bq_table="source_data.auth_table"

For parallel multi threaded execution make sure you create different input files with changes to the necessary input values. 

Step5: Execute the commands to generate the data 

Execution should follow a sequence. The customer data generation process generates a merchant to cc token mapping file. This file is required for generating co-related data. 

    
    bash generate_customer_data.sh  # needs to be run 1st

    bash generate_merchant_data.sh  

    bash generate_transaction_data.sh
    

## TODOs:
1. Generate credit card events data e.g. https://jis-eurasipjournals.springeropen.com/articles/10.1186/s13635-018-0076-9/figures/4
2. Add fraud indicator and add a module to generate cc to mapping data to generate fraudulent transactions
3. Other data - terminal_ids
