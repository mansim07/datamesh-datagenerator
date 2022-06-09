

if [ "$#" -ne 6 ]; then
    echo "Illegal number of parameters"
    exit 1
fi

part_val=$1
data_dir_val=$2
project_val=$3
customers_bucket_val=$4
merchants_bucket_val=$5
transactions_bucket_val=$6


sed -i '' -e "s/\(write_.*_to_cloud=\).*/\1\"false\"/" inputs.sh
sed -i '' -e "s/\(date_partition=\).*/\1\"${part_val}\"/" inputs.sh
sed -i '' -e "s/\(local_data_dir=\).*/\1\"${data_dir_val}\"/" inputs.sh
sed -i '' -e "s/\(.*_project=\).*/\1\"${project_val}\"/" inputs.sh
sed -i '' -e "s/\(customer_bucket=\).*/\1\"${customers_bucket_val}\"/" inputs.sh
sed -i '' -e "s/\(merchant_bucket=\).*/\1\"${merchants_bucket_val}\"/" inputs.sh
sed -i '' -e "s/\(credit_card_bucket=\).*/\1\"${transactions_bucket_val}\"/" inputs.sh

