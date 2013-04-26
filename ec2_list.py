#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto.ec2

connection = boto.ec2.connect_to_region("us-west-1")
for serv in [x.instances[0] for x in connection.get_all_instances()]:
    if serv.state_code == 16:
        name = serv.tags.get('Name', 'None')
        print "{} is instance {}".format(name, serv.id)
