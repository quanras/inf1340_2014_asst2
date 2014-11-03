#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim / Evan Moir'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim / Evan Moir"
__license__ = "MIT License"

__status__ = "Final Submission"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
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
    if len(traveler_records) is 0:
        return decision_list

    # Loop through the traveler_records and add the decision for each entry to the decision_list.
    # Priority: Quarantine, Reject, Secondary Processing, Accept.
    for record in traveler_records:

        # Check for Quarantine condition.
        if has_medical_advisory(record[], record[], medical_advisories):
            decision_list.append("Quarantine")

        # Check for Rejection conditions.
        elif not record_valid(record):
            decision_list.append("Reject")

        elif visitor_visa_required(record[], record[], visitor_visas) or transit_visa_required(record[], record[], transit_visas):
            if not record_valid(record) or not valid_date_format(record[]) or not visa_date_valid(record[]):
                decision_list.append("Reject")

        # Check for Secondary Processing conditions.
        elif on_watchlist(entry, watchlist):
            decision_list.append("Secondary")

        # Accept if none of the other conditions have been met.
        else:
            decision_list.append("Accept")

    return decision_list


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False

def visa_date valid(visa_date):
    """
    :param: visa date, the date field from the record entry's visa.
    :return: Boolean; True is the visa contains all required fields, has a valid date field and was issued in the
                    last two years, False otherwise.
    """
    if valid_date_format(visa_date) and (#Deal with data calculation here):
        return True
    else:
        return False



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
def record_valid(record):
    """
    :param record:
    :return: Boolean; True if the entry record has all required information (First Name, Last Name, Birth Date,
                Passport Number (w correct format), Home, From, Reason for Entry), False otherwise.
    """
    if not record['first_name'] is '' and not record['last_name'] is '' \
        and valid_passport_format(record['passport'])

# Check if the record entry is on the watchlist (name or passport)
def on_watchlist(first_name, last_name, passport_number, watchlist):
    """
    :param first_name:
    :param last_name:
    :param passport_number:
    :param watchlist:
    :return:
    """

# Check if a record entry is a citizen returning home.
def returning_home(home_string, reason_for_entry):
    """
    :param home_string:
    :param reason_for_entry:
    :return: True if the entry record has Home == "KAN" and Reason for Entry == "returning", False otherwise.
    """

# Check if a record entry requires a visitor visa
def visitor_visa_required(reason_for_entry, home_country, visitor_visa_list):
    """
    :param reason_for_entry:
    :param watchlist:
    :return:
    """


# Check if a record entry requires a transport visa
def transit_visa_required(reason_for_entry, home_country, transit_visa_list):
    """
    :param passport_number:
    :param countries:
    :return:
    """


def has_medical_advisory(home_country, from_country, medical_advisories):
    """
    :param home_string:
    :param from_string:
    :param watchlist:
    :return: Boolean; True if either of the record's Home or From Locations have a Medical Advisory, False otherwise.
    """