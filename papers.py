#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Evan Moir'
__email__ = 'evan.moir@utoronto.ca'

__copyright__ = '2014 Susan Sim / Evan Moir'
__license__ = 'MIT License'

__status__ = 'Final Submission'

# imports one per line
import re
import json
import datetime


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains the immigration records requiring decisions.
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist.
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings representing the immigration decision, one for each record.
    Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """


    # Read in input_file
    traveler_records = json.loads(input_file)

    # Read in watchlist_file
    watchlist = json.loads(watchlist_file)

    # Read in countries_file
    all_countries = json.loads(countries_file)

    # Make separate lists for medical advisories, visitor visa and transit visa requirements.
    medical_advisories = []
    visitor_visas = []
    transit_visas = []

    for country in all_countries:
        if country['medical advisory'] is not '':
            medical_advisories.append(country)

        if country['visitor_visa_required'] is 1:
            visitor_visas.append(country)

        if country['transit_visa_required'] is 1:
            transit_visas.append(country)

    # Create empty decision_list to hold decision(s); return decision_list empty if traveler_records is empty.
    decision_list = []
    if traveler_records.len() is 0:
        return decision_list

    # Loop through the traveler_records and add the decision for each entry to the decision_list.
    # Priority: Quarantine, Reject, Secondary Processing, Accept.
    for record in traveler_records:

        # Check for Quarantine condition.
        if has_medical_advisory(record['home']['country'], record['from']['country'], medical_advisories):
            decision_list.append('Quarantine')

        # Check for Rejection condition (incomplete record)
        elif not complete_record(record):
            decision_list.append('Reject')

        # Check for Rejection condition (travel visa required but not present, or invalid/expired)
        elif visitor_visa_required(record['entry_reason'], record['home']['country'], visitor_visas):
            if not 'visa' in record or not valid_visa_date(record['visa']):
                decision_list.append('Reject')

        # Check for Rejection condition (transit visa required but not present, or invalid/expired)
        elif transit_visa_required(record['entry_reason'], record['from']['country'], transit_visas):
            if not 'visa' in record or not valid_visa_date(record['visa']):
                decision_list.append('Reject')

        # Check for Secondary Processing conditions.
        elif on_watchlist(record['first_name'], record['last_name'], record['passport'], watchlist):
            decision_list.append('Secondary')

        # Accept if none of the non-Accept conditions have been met.
        else:
            decision_list.append('Accept')

    return decision_list


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('^\w{5}-\w{5}-\w{5}-\w{5}-\w{5}$')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_visa_format(visa):
    """
    :param visa: the record's visa
    :return: Boolean; True if the visa is valid (has a valid code and was issued less than two years ago).
    """
    visa_format = re.compile('^\w{5}-\w{5}$')

    if visa_format.match(visa['date']):
        return True
    else:
        return False


# A method to check if a visa is valid (has a valid date, and was issued in the last two years).
# Admittedly, this function does not take the possibility of leap years into account.
def valid_visa_date(visa):
    """
    :param visa: the record's visa
    :return: Boolean; True if the visa's date is valid and the via was issued in the last two years, False otherwise.
    """
    if valid_date_format(visa['date']):
        visa_date = datetime.date(visa['date'][0:4], visa['date'][5:7], visa['date'][8:10])

        # Check if the visa issue date was in the past two years.
        if 0 < datetime.datetime.today() - visa_date <= 730:
            return True
    return False


# Check a date string for the correct format.
def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean; True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Check if a record entry contains the minimum numbers of fields for it to have basic validity.
def complete_record(record):
    """
    :param record: the record being checked for validity.
    :return: Boolean; True if the entry record has all required information (First Name, Last Name, Birth Date,
                Passport Number (w correct format), Home, From, Reason for Entry), False otherwise.
    """
    valid_entry_reasons = ['visit', 'transit', 'returning']

    if not 'first_name' in record.keys() or record['first_name'] is '':
        return False
    elif not 'last_name' in record.keys() or record['last_name'] is '':
        return False
    elif not 'birth_date' in record.keys() or not valid_date_format(record['birth_date']):
        return False
    elif not 'passport' in record.keys() or not valid_passport_format(record['passport']):
        return False
    elif not 'home' in record.keys():
        return False
    elif not 'from' in record.keys():
        return False
    elif not 'entry_reason' in record.keys():
        return False
    elif not record['entry_reason'] in valid_entry_reasons:
        return False
    return True


# Check if the record entry is on the watchlist (name or passport)
def on_watchlist(first_name, last_name, passport, watchlist):
    """
    :param first_name: the record's first_name entry
    :param last_name: the record's last_name entry
    :param passport: the record's passport
    :param watchlist: the watchlist JSON object
    :return: Boolean; True if the record's first and last name or passport are on the Watchlist, False otherwise.
    """
    for watchlist_item in watchlist:
        if watchlist_item['first_name'] == first_name and watchlist_item['last_name'] == last_name:
            return True
        elif watchlist_item['passport'] == passport:
            return True
        else:
            return False


# Check if a record entry is a citizen returning home.
def returning_home(home_country, reason_for_entry):
    """
    :param home_country: the record's home country entry.
    :param reason_for_entry: the record's entry_reason entry.
    :return: Boolean, True if the record has home_country equal to KAN and reason_For_entry equal to returning;
    False otherwise.
    """
    if home_country == 'KAN' and reason_for_entry == 'returning':
        return True
    return False


# Check if a record entry requires a visitor visa
def visitor_visa_required(reason_for_entry, home_country, visitor_visa_list):
    """
    :param reason_for_entry: the record's entry_reason entry
    :param home_country: the record's home country
    :param visitor_visa_list: the visitor visa list
    :return: Boolean; True if the record requires a visitor visa, False otherwise.
    """
    if reason_for_entry == 'visit':
        for country in visitor_visa_list:
            if home_country == country['code']:
                return True
    return False


# Check if a record entry requires a transport visa
def transit_visa_required(reason_for_entry, home_country, transit_visa_list):
    """
   :param reason_for_entry: the record's entry_reason string
   :param home_country: the entry's home_country
   :param transit_visa_list:
   :return: True if the record requires an transit visa, False otherwise.
   """
    if reason_for_entry == 'transit':
        for country in transit_visa_list:
            if home_country == country:
                return True
    return False


def has_medical_advisory(home_country, from_country, medical_advisories):
    """
   :param home_country: the record's home country.
   :param from_country: the record's from country.
   :param medical_advisories: the list of countries with medical advisories.
   :return:
   """
    for country in medical_advisories:
        if home_country == country or from_country == country:
            return True
    return False