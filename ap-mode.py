#!/usr/bin/env python

from netmiko import ConnectHandler
import string

#
# SSH Config:
#
with ConnectHandler(ip = '10.132.0.100',
        port = 22,
        username = 'adm140980',
        password = 'Password',
        device_type = 'cisco_wlc_ssh') as ch:
#
# Send command to disable paging
#
    ch.send_command_timing("config paging disable")
    output = ch.send_command_timing("show ap summary")
#
# Take the output from show ap summary, and remove the first 9 lines (this is a bad way to do it, but i'm lazy).  It's done so we only have the list of AP and no headers or useless info
#
    postString = output.split("\n",9)[9]
#
# Partition the string, based on whitespace, and take the first value (not used)
#
#    trimmed = postString.partition(" ")[0]

#
# Split the variable by line
#
    content = postString.split("\n")
#
# Split the line so that we take only the AP name
#
    content = [i.split(' ')[0] for i in content]

#
# Loop through each AP Name and execute the following:
#
    for i in content:
        apname = i
        apconfig = "show ap config general " + i
        apresult = ch.send_command_timing(apconfig)

# We take the AP config command, split by line, then seach for AP Mode, partition and take only the result of AP mode (Flex Connect or Local)

        for item in apresult.split("\n"):
            if "AP Mode " in item:
                mode = item.strip()
                trimapmode = mode.partition(". ")[2]
#
# Print the result, one AP per line because we're still in the foreach loop
#
                print(apname + " " + trimapmode)