source inputs.sh

mkdir -p ${local_data_dir}


python3 ./customer_data/create_customers_cc_merchant.py ${num_of_customers} ${customer_seed} ${profile_name} ${local_data_dir}/${customer_file} ${local_data_dir}/${cc_customer_file} ${local_data_dir}/${cc_merchant_file} ${customer_project} ${customer_bucket} ${customer_gcs_file} ${cc_customer_map_gcs_file}
res=$?

if [ $res -eq 0 ];
then
bq rm -t -f --project_id=${customer_project} ${customer_bq_table}
bq rm -t -f --project_id=${customer_project} ${cc_customer_map_bq_table}


bq load \
--project_id=${customer_project} \
--autodetect \
--source_format=CSV \
--field_delimiter="|" \
--skip_leading_rows=1 \
--allow_quoted_newlines \
--allow_jagged_rows \
${customer_bq_table} gs://${customer_bucket}/${customer_gcs_file}

bq load \
--project_id=${customer_project} \
--autodetect \
--source_format=CSV \
--field_delimiter="|" \
--skip_leading_rows=1 \
--allow_quoted_newlines \
--allow_jagged_rows \
${cc_customer_map_bq_table} gs://${customer_bucket}/${cc_customer_map_gcs_file}
fi


cust(){

python3 ./merchant_data/create_merchants.py 10000 ${seed} ${local_data_dir}/merchant.csv ${mcc_file_name} ${cc_merchant_filename} ${merchant_project} ${merchant_bucket} ${merchant_gcs_filename} ${mcc_gcs_filename}

#if [ $? -ne 0 ];
#then
bq rm -t -f --project_id=${merchant_project} merchants_source_data.core_merchants
bq rm -t -f --project_id=${merchant_project} merchants_reference_data.mcc_code


bq load \
--project_id=${merchant_project} \
--autodetect \
--source_format=CSV \
--field_delimiter="|" \
--skip_leading_rows=1 \
--allow_quoted_newlines \
--allow_jagged_rows \
merchants_source_data.core_merchants gs://${merchant_bucket}/${merchant_gcs_filename}

bq load \
--project_id=${merchant_project} \
--autodetect \
--source_format=CSV \
--field_delimiter="," \
--skip_leading_rows=1 \
--allow_quoted_newlines \
--allow_jagged_rows \
merchants_reference_data.mcc_code gs://${merchant_bucket}/${mcc_gcs_filename}
#fi




python3 ./transaction_data/create_transactions.py 50 430 /Users/maharanam/OpenSourceCode/datamesh-datagenerator/customer_data/data/cc_merchant_info_for_trans.csv /Users/maharanam/OpenSourceCode/datamesh-datagenerator/transaction_data/data/trans_data.csv 2022-01-01 2022-02-02 bankofmars-retail-credit-cards bankofmars_retail_credit_cards_trasactions_data "auth_trans/date=${date_partition}/auth.csv"

}
