'''
    Schema: 
        Merchant Name 
        Merchant Address
        Merchant Phone Number 
        Merchant Category Code 
        Merchant Latitude 
        Merchant Longitude  
'''

import math
from operator import ne
import faker
from faker import Faker
import random
import numpy as np
import sys
import datetime
from datetime import date
from datetime import timedelta
import fileinput
import random
from collections import defaultdict
import json
#import demographics
#from main_config import MainConfig
from datetime import timezone, datetime
import csv
from faker_credit_score import CreditScore
import os
import glob
from csv import reader
import time


class Transactions:
    print("Inside Class")
    def __init__(self, row, counter,terminal_list):
        self.cc_token=row[5]
        self.card_read_type=5
        date_time=fake.date_time_between(start_date='-3d',end_date='now')
        self.trans_ts=time.mktime(date_time.timetuple())
        #self.trans_time=fake.time()
        self.trans_type=1
        self.trans_amount=fake.pricetag().replace('$','')
        self.trans_currency="USD"
        self.trans_auth_code=fake.random_number(digits=6,fix_len=True)
        self.trans_auth_date= self.trans_ts
        self.payment_method=random.choice([1,2,3,4,5,6,7,8,9,10,11])
        self.origination=1
        self.is_pin_entry=random.choice([0,1])
        self.is_signed=random.choice([0,1])
        self.is_unattended=random.choice([0,1])
        self.swipe_type=random.choice([0,1])
        self.terminal_id=random.choice(terminal_list)
        self.event_ids=fake.uuid4()
        self.event=""
 

    def get_merchant_name(self,row):
        if row[5] == 'Y':
            return row[1]
        else:
            return fake.company() + " " + row[1].split(' ')[0] + " " + fake.company_suffix()



def validat_parse_input():
    def print_err(n):
        if n == 1:
            print('Error: invalid number of customers')
        elif n == 2:
            print('Error: invalid (non-integer) random seed')
        elif n == 3:
            print('Error: main.config could not be opened')

        output = '\nENTER:\n (1) Number of customers\n '
        output += '(2) Random seed (int)\n '
        output += '(3) main_config.json\n'
        output += '(4) GCP project_name\n'
        output += '(5) GCS bucket_name'

        print(output)
        sys.exit(0)

    try:
        num_trans_per_customer = int(sys.argv[1])
    except:
        print_err(1)
    try:
        seed_num = int(sys.argv[2])
    except:
        print_err(2)
    try:
        cc_customer_file = sys.argv[3]
        #merchant_output_filename = open(m, 'r').read()
    except:
        print_err(3)
    try:
        customer_file = sys.argv[4]
        #merchant_output_filename = open(m, 'r').read()
    except:
        print_err(3)
    try:
        merchant_file_name = sys.argv[5]
        #merchant_mcc_codes= open(m1, 'r').read()
    except:
        print_err(4)
    try:
        transactions_output_filename = sys.argv[6]
    except:
        print_err(5)

    try:
        start_date = sys.argv[7]
    except:
        print_err(5)

    try:
        end_date = sys.argv[8]
    except:
        print_err(5)
    try:
        project_id = sys.argv[9]
    except:
        print_err(5)
    try:
        bucket_name = sys.argv[10]
    except:
        print_err(5)

    return  num_trans_per_customer, seed_num, cc_customer_file, merchant_file_name, transactions_output_filename, start_date, end_date,  project_id, bucket_name

if __name__ == '__main__':
    #create transaction and transaction history
    num_trans_per_customer, seed_num, cc_customer_file, merchant_file_name, transactions_output_filename, start_date, end_date,  project_id, bucket_name = validat_parse_input()


    #merchant_source_filename=sys.argv[1]    #"./data/merchant.csv"
    #merchant_mcc_codes=sys.argv[2]

    #generate transaction event file 
    #event_code, event_id, timestamp, value 
    #generate transaction file 
    #Put event_id here 
    #for now generate one file 

    fake = Faker()
    Faker.seed(10)
    #Create a sample terminal_id to cc_token mapping based on location
    #can be done in Spark 

    terminal_list=[]
    with open("/Users/maharanam/OpenSourceCode/datamesh-datagenerator/merchant_data/data/merchant.csv", 'r') as read_obj:
        csv_reader = reader(read_obj,delimiter='|')
        header = next(csv_reader)

        for row in csv_reader:
            terminal_list.append(eval(row[13])[0])

    with open("/Users/maharanam/OpenSourceCode/datamesh-datagenerator/customer_data/data/cc_customer.csv", 'r') as read_obj:
        csv_reader = reader(read_obj,delimiter='|')
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            count=0
            with open("/Users/maharanam/OpenSourceCode/datamesh-datagenerator/transaction_data/data/trans_data.csv", 'w', newline='') as transactionfile:
                transactions_fieldnames = ['cc_token','card_read_type', 'trans_ts', 'trans_type', 'trans_amount',
                               'trans_currency',  'trans_auth_code', 'trans_auth_date', 'payment_method', 'origination','is_pin_entry', 'is_signed','is_unattended','swipe_type', 'terminal_id','event_ids','event']

                transaction_writer = csv.DictWriter(
                transactionfile, delimiter=';', lineterminator='\n', fieldnames=transactions_fieldnames,  quotechar='"', doublequote=True)

                transaction_writer.writeheader()

                for row in csv_reader:
                    # row variable is a list that represents a row in csv
                    count=count+1 
                    for _ in range(10):

                        new_data = Transactions(row,count,terminal_list)
                        transaction_writer.writerow({
                            'cc_token': new_data.cc_token,
                            'card_read_type': new_data.card_read_type,
                            'trans_ts': new_data.trans_ts,
                            'trans_type': new_data.trans_type,
                            'trans_amount': new_data.trans_amount,
                            'trans_currency': new_data.trans_currency,
                            'trans_auth_code': new_data.trans_auth_code,
                            'trans_auth_date': new_data.trans_auth_date,
                            'payment_method': new_data.payment_method,
                            'origination': new_data.origination,
                            'is_pin_entry': new_data.is_pin_entry,
                            'is_signed': new_data.is_signed,
                            'is_unattended':new_data.is_unattended,
                            'swipe_type':new_data.swipe_type,
                            'terminal_id': new_data.terminal_id,
                            'event_ids':new_data.event_ids,
                            'event':new_data.event




                        }
                        )

                    #if count == num_trans_per_customer: 
                   #     break



