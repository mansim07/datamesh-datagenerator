#date value for gcs path 
date_partition=2020-10-10
local_data_dir="/tmp/data/"

#Customer Inputs
customer_project="bankofmars-retail-customers"
customer_bucket="bankofmars_retail_customers_source_data"
customer_bq_table="raw_data.customer_demographics"
cc_customer_map_bq_table="raw_data.cc_customer_data"
customer_seed=10
num_of_customers=2000
profile_name="./profiles/main_config.json"
customer_hive_parent="customers_data"
cc_customer_parent="cc_customers_data"
customer_file=customer.csv
cc_customer_file=cc_customer.csv
cc_merchant_file=cc_merchant_info_for_trans.csv
customer_gcs_file="${customer_hive_parent}/dt=${date_partition}/${customer_file}"
cc_customer_map_gcs_file="${cc_customer_parent}/dt=${date_partition}/${cc_customer_file}"

#Merchant Inputs
merchant_project="bankofmars-retail-merchants"
merchant_bucket="bankofmars_retail_merchants_data"
merchant_seed=20
num_merchants=1000
cc_merchant_data="merchants_data"
ref_data_local_path="./merchant_data/data/ref_data"
mcc_file_name="mcc_codes.csv"
merchant_filename="merchants.csv"
merchant_gcs_filename="${cc_merchant_data}/date=${date_partition}/${merchant_filename}"
mcc_gcs_filename="mcc_codes/date=${date_partition}/${mcc_file_name}"
#make sure "cc_merchant_file" is set
merchant_bq_table="raw_data.core_merchants"
mcc_bq_table="merchants_reference_data.mcc_code"


#Credit Card Transactions Inputs
credit_card_project="bankofmars-retail-credit-cards"
credit_card_bucket="bankofmars_retail_credit_cards_trasactions_data"
cc_ref_bq_dataset="lookup_data"
cc_hive_parent="auth_data"
num_of_trans_per_cust=3
cc_trans_seed=30
trans_filename=trans_data.csv
cc_auth_gcs_path="${cc_hive_parent}/date=${date_partition}/${trans_filename}"
start_date=2020-10-01
end_date=2022-10-10
trans_ref_data="./transaction_data/data/ref_data"
auth_bq_table="source_data.auth_table"