#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from boto.route53 import *
import boto.route53.record
import urllib2
import time
import httplib

# noinspection PyStatementEffect
"""

A boto stub to dig through an entire (presumably over-sized) route53 account
and index every last A & CNAME record, then do a web grab to collect the status
and destination url. Of course dump everything as a CSV.

I coulda wrote this as a proper class but it's a stub damnit.

Created by bunnyman on 2013/02/11.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""

output_file = "Domains.csv"


def main():
    my_key = ""
    my_secret = ""

    connection = Route53Connection(
        aws_access_key_id=my_key, aws_secret_access_key=my_secret)

    zones = connection.get_zones()

    with open(output_file, 'w') as outfile:
        print("Domain,Type,Destination,Status Code,Destination URL", file=outfile)
        domain_count = len(zones)
        for zone in zones:
            print("Checking: #{}; {}".format(domain_count, zone))
            domain_count -= 1

            records = zone.get_records()
            for record in records:
                assert isinstance(record, boto.route53.record.Record)
                if record.type != u'A' and record.type != u'CNAME':
                    continue

                domain = record.name[:-1]
                record_type = record.type
                destination = record.to_print()
                destination_url = ""
                return_code = ""

                # Handle *.domain.com without a query
                if domain[0:4] == u'\\052':
                    domain = "*.{}".format(domain[5:])
                    print("{},{},{},Star records are not queried".format(
                        domain, record_type, destination), file=outfile
                    )
                    outfile.flush()  # Waisting time to keep API limits happy
                    continue

                req = urllib2.Request("http://{}/".format(domain))
                try:
                    site = urllib2.urlopen(req)
                    return_code = site.getcode()
                    destination_url = site.geturl()
                except urllib2.HTTPError as e:
                    return_code = e.code
                except urllib2.URLError as e:
                    return_code = e.reason
                except httplib.BadStatusLine as e:
                    return_code = e.message

                print("{},{},{},{},{}".format(
                    domain, record_type, destination,
                    return_code, destination_url), file=outfile
                )
                outfile.flush()  # Waisting time to keep API limits happy

            time.sleep(2)  # AWS API will server side throttle if we don't


if __name__ == '__main__':
    main()

__author__ = 'bunnyman'
