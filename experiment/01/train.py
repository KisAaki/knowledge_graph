#-*-coding:UTF-8 -*-

import os
import csv
import re
import logging
import optparse

import dedupe
from unidecode import unidecode

if __name__ == "__main__":
    # Define the fields dedupe will pay attention to
    fields = [
        {'field': 'Name', 'type': 'String'},
        {'field': 'id', 'type': 'Int'},
        #{'field': 'Zip', 'type': 'Exact', 'has missing': True},
        #{'field': 'Phone', 'type': 'String', 'has missing': True},
    ]

    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)

    dedupe.console_label(deduper)

    # Using the examples we just labeled, train the deduper and learn
    # blocking predicates
    deduper.train()

    pass