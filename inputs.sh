#date value for gcs path 
date_partition=2020-10-20
local_data_dir="/tmp/data/"

#Must Replace
customer_project="bankofmars-retail-customers"
customer_bucket="bankofmars_retail_customers_source_data"
customer_bq_table="customers_source_data.customer_demographics"
cc_customer_map_bq_table="customers_source_data.cc_customer_data"

merchant_project="bankofmars-retail-merchants"
merchant_bucket="bankofmars_retail_merchants_data"
credit_card_project="bankofmars-retail-credit-cards"
credit_card_bucket="bankofmars_retail_credit_cards_trasactions_data"

#Customer Inputs
customer_seed=1
num_of_customers=1000
profile_name="./profiles/main_config.json"

customer_file=customer.csv
cc_customer_file=cc_customer.csv
cc_merchant_file=cc_merchant_info_for_trans.csv
customer_gcs_file="customers_data/date=${date_partition}/${customer_file}"
cc_customer_map_gcs_file="cc_customers_data/date=${date_partition}/${cc_customer_file}"



#Merchant Inputs
merchant_seed=1
num_merchants=1000

mcc_local_path="./data/ref_data"
mcc_file_name="mcc_codes.csv"
merchant_filename="merchants.csv"
merchant_gcs_path="merchants_data/date=${date_partition}/${merchant_filename}"
mcc_gcs_path="mcc_codes/date=${date_partition}/${mcc_file_name}"
#make sure "cc_merchant_file" is set



#Credit Card Transactions Inputs
num_of_trans_per_cust=10
cc_seed=1

trans_filename=trans_data.csv
cc_auth_gcs_path="auth_data/date=${date_partition}/${trans_filename}"
start_date=2022-01-01
end_date=2022-01-02