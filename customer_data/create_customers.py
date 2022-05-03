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
import demographics
from main_config import MainConfig
from datetime import timezone, datetime
import csv
#from faker_credit_score import CreditScore
import os
import glob
import hashlib

from google.cloud import storage

# def write_file():


class Headers:
    'Store the headers and print to stdout to pipe into csv'

    def __init__(self):
        self.make_headers()
        self.print_headers()

    def make_headers(self):
        headers = ''
        for h in ['client_id', 'ssn', 'cc_num', 'acct_num', 'first', 'last', 'gender', 'street',
                  'city', 'state', 'zip', 'latitude', 'longitude', 'city_pop',
                  'job', 'dob', 'email', 'phonenum', 'profile']:
            headers += h + '|'
        self.headers = headers[:-1]

    def print_headers(self):
        print(self.headers)


class Customer:
    'Randomly generates all the attirubtes for a customer'

    def __init__(self):

       # self.cust_id = fake.unique.random_int(min=0, max=num_cust+50000)
        self.client_id = fake.uuid4()
        self.cc = fake.unique.credit_card_number()
        self.account = fake.random_number(digits=12)

        # Customer Data
        self.ssn = fake.ssn()
        self.gender,self.dob = self.generate_age_gender()
        self.first = self.get_first_name()
        self.last = fake.last_name()
        self.street = fake.street_address()
        self.addy = self.get_random_location()
        self.job = fake.job()
        self.email = self.first.lower() + "." + self.last.lower() + \
            "@" + fake.free_email_domain()
        self.profile = self.find_profile()
        self.phonenum = fake.phone_number()

        # Credit Card Type
        self.cc_provider = fake.credit_card_provider()
        self.cc_expiry = fake.credit_card_expire(
            start="-10y", end="+10y", date_format="%m/%y")
        self.cc_ccv = fake.credit_card_security_code()
        self.cc_cardtype = self.get_card_type()
        token_str= hashlib.sha256((self.cc + self.cc_expiry + 'E1F53135E559C253').encode())
        self.token=token_str.hexdigest() #token=SHA256(PAN|EXP_DATE|SSS)

        # Fico Score
        # Generate as seperate job

        self.print_customer()

    def get_first_name(self):
        if self.gender == 'M':
            return fake.first_name_male()
        else:
            return fake.first_name_female()

    def get_card_type(self):
        card_type = ['Gold', 'Platinum', 'Classic']
        age = (date.today() - self.dob).days / 365.25
        if age <= 18:
            return 'Junior'
        else:
            return random.choice(card_type)

    def generate_age_gender(self):
        #g_a = age_gender[min([a for a in age_gender if a > np.random.random()])]
        #g_a = age_gender[min(age_gender, key=lambda x:abs(x-random.random()))]

        a = np.random.random()
        c = []
        for b in age_gender.keys():
            if b > a:
                c.append(b)
        g_a = age_gender[min(c)]

        while True:
            dob = fake.date_time_this_century()

            # adjust the randomized date to yield the correct age
            start_age = (date.today() - date(dob.year,
                         dob.month, dob.day)).days / 365.
            dob_year = dob.year - int(g_a[1] - int(start_age))

            # since the year is adjusted, sometimes Feb 29th won't be a day
            # in the adjusted year
            try:
                # return first letter of gender and dob
                return g_a[0][0], date(dob_year, dob.month, dob.day)
            except:
                pass

    # find nearest city
    def get_random_location(self):
        return cities[min(cities, key=lambda x: abs(x - random.random()))]

    def find_profile(self):
        age = (date.today() - self.dob).days / 365.25
        city_pop = float(self.addy.split('|')[-1])

        match = []
        for pro in all_profiles:
            # -1 represents infinity
            if self.gender in all_profiles[pro]['gender'] and \
                age >= all_profiles[pro]['age'][0] and \
                    (age < all_profiles[pro]['age'][1] or
                     all_profiles[pro]['age'][1] == -1) and \
                city_pop >= all_profiles[pro]['city_pop'][0] and \
                    (city_pop < all_profiles[pro]['city_pop'][1] or
                     all_profiles[pro]['city_pop'][1] == -1):
                match.append(pro)
        if match == []:
            match.append('leftovers.json')

        # found overlap -- write to log file but continue
        if len(match) > 1:
            f = open('profile_overlap_warnings.log', 'a')
            output = ' '.join(match) + ': ' + self.gender + ' ' + \
                     str(age) + ' ' + str(city_pop) + '\n'
            f.write(output)
            f.close()
        return match[0]

    def get_customer(self):
        value = str(self.client_id) + '|' + \
            str(self.ssn) + '|' + \
            str(self.cc) + '|' + \
            str(self.account) + '|' + \
            self.first + '|' + \
            self.last + '|' + \
            self.gender + '|' + \
            self.street + '|' + \
            self.addy + '|' + \
            self.job + '|' + \
            str(self.dob) + '|' + \
            str(self.email) + '|' + \
            str(self.phonenum) + '|' + \
            self.profile

        return value

    def print_customer(self):
        value = str(self.client_id) + '|' + \
            str(self.ssn) + '|' + \
            str(self.cc) + '|' + \
            str(self.account) + '|' + \
            self.first + '|' + \
            self.last + '|' + \
            self.gender + '|' + \
            self.street + '|' + \
            self.addy + '|' + \
            self.job + '|' + \
            str(self.dob) + '|' + \
            str(self.email) + '|' + \
            str(self.phonenum) + '|' + \
            self.profile

        # print(value)


def validate():
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
        num_cust = int(sys.argv[1])
    except:
        print_err(1)
    try:
        seed_num = int(sys.argv[2])
    except:
        print_err(2)
    try:
        m = sys.argv[3]
        main = open(m, 'r').read()
    except:
        print_err(3)
    try:
        project_id = sys.argv[4]
    except:
        print_err(4)
    try:
        bucket_name = sys.argv[5]
    except:
        print_err(5)

    return num_cust, seed_num, main, project_id, bucket_name


if __name__ == '__main__':
    # read and validate stdin
    num_cust, seed_num, main, project_id, bucket_name = validate()
    

    # from demographics module
    cities = demographics.make_cities()
    age_gender = demographics.make_age_gender_dict()

    fake = Faker()
    Faker.seed(seed_num)
    #fake.add_provider(CreditScore)

    #headers = Headers()

    # turn all profiles into dicts to work with
    all_profiles = MainConfig(main).config

    today_date = datetime.today().strftime('%Y-%m-%d')
    ts = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    client = storage.Client(project=project_id)
    bucket = client.get_bucket(bucket_name)
    customer_file = "customers_data/date=" + today_date + "/customer_" + str(ts) + ".csv"
    cc_customer_file= "cc_customers_data/date=" + today_date + "/cc_customer_" + str(ts) + ".csv"
    customer_blob = bucket.blob(customer_file)
    cc_customer_blob = bucket.blob(cc_customer_file)
    customer_source_filename="./data/customer.csv"
    cc_customer_source_filename="./data/cc_customer.csv"

    with open(customer_source_filename, 'w', newline='') as customerfile, open(cc_customer_source_filename, 'w', newline='') as cc_custfile:
        customer_fieldnames = ['client_id', 'ssn', 'first_name', 'last_name', 'gender', 'street', 'city',
                               'state', 'zip', 'latitude', 'longitude', 'city_pop', 'job', 'dob', 'email', 'phonenum', 'profile']
        customer_writer = csv.DictWriter(
            customerfile, delimiter='|', lineterminator='\n', fieldnames=customer_fieldnames)

        customer_writer.writeheader()

        cc_customer_fieldnames = [
                'cc_number', 'cc_expiry', 'cc_ccv', 'cc_card_type', 'client_id','token']
        cc_customer_writer = csv.DictWriter(
                cc_custfile, delimiter='|', lineterminator='\n', fieldnames=cc_customer_fieldnames)

        cc_customer_writer.writeheader()
        for _ in range(num_cust):
            new_data = Customer()
            customer_writer.writerow({
                'client_id': new_data.client_id,
                'ssn': new_data.ssn,
                'first_name': new_data.first,
                'last_name': new_data.last,
                'gender': new_data.gender,
                'street': new_data.street,
                'city': new_data.addy.split('|')[0],
                'state': new_data.addy.split('|')[1],
                'zip': new_data.addy.split('|')[2],
                'latitude': new_data.addy.split('|')[3],
                'longitude': new_data.addy.split('|')[4],
                'city_pop': new_data.addy.split('|')[5],
                'job': new_data.job,
                'dob': new_data.dob,
                'email': new_data.email,
                'phonenum': new_data.phonenum,
                'profile': new_data.profile
            }
            )



            cc_customer_writer.writerow({
                'cc_number': new_data.cc,
                'cc_expiry': new_data.cc_provider,
                'cc_ccv': new_data.cc_ccv,
                'cc_card_type': new_data.cc_cardtype,
                'client_id': new_data.client_id,
                'token': new_data.token

            }
            )
    customer_blob.upload_from_filename(customer_source_filename)
    cc_customer_blob.upload_from_filename(cc_customer_source_filename)

    #files = glob.glob('./data/*')
    #for f in files:
    #    os.remove(f)

