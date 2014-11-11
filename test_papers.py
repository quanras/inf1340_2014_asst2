#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
import papers


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")

# add functions for other tests

def test_valid_visa_date():
    assert valid_visa_date({'date': '1999-10-01'}) == False
    assert valid_visa_date({'date': '2014-10-31'}) == True
    assert valid_visa_date({'date': '2012-12-31'}) == True
    assert valid_visa_date({'date': True}) == False
    assert valid_visa_date({'date': '!!!!-PP-<>'}) == False

complete_record = {'first_name': "First!",
                   'last_name': "Last!",
                   'birth_date': "1982-09-26",
                   'passport': '3Z416-ZM6NW-ZO5WV-EVHYS-VPGAZ',
                   'home': {
                        'city': 'Urella',
                        'region':'  Parsol',
                        'country':'GOR'
                        },
                   "from":{
                        "city":"Urella",
                        "region":"Parsol",
                        "country":"GOR"
                            },
                    "entry_reason":"visit"
                   }
incomplete_record = {}
def test_complete_record():
    assert complete_record(complete_record) == True
    assert complete_record(incomplete_record) == False

def test_on_watchlist():
    assert on_watchlist("PATRIA", "OGLESBY", "Passport", 'watchlist.json') == True
    assert on_watchlist("Evan", "Moir", "Passport", 'watchlist.json') == False
    assert on_watchlist("Evan", "Moir", "QEMSB-PS4OG-3CV7S-8XKLZ-Y4XM2", 'watchlist.json') == True


