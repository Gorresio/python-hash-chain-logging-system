#
# Copyright (c) 2019, Stefano Gorresio <stefano.gorresio@null.net>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the python-hash-chain-logging-system project.
#


from sys import argv, exit
from time import time
from datetime import datetime
from random import random
from hashlib import sha256
import sqlite3



def print_exit(text):
    print(text)
    exit()


def print_info():
    print("\n")
    print("\t    ** hash-chain-logging-system **\n")
    print("\tAuthor: Stefano Gorresio")
    print("\tVersion: python alpha 0.1")
    print("\tLicense: GPLv3")
    print("\tSource Code: https://github.io/Gorresio/python-hash-chain-logging-system")
    print("\n")
    exit()


def print_help():
    print("\n")
    print("\t -f <filename>        Select log file.")
    print("\t --add <text>         Text to insert.")
    print("\t --show               Show logs.")
    print("\t --where <conditions> Custom SQL WHERE for \"--show\" and \"--csv-dump\" options.")
    print("\t --query <query>      Custom SQL query (no output).")
    print("\t --verify-integrity   Check file integrity.")
    print("\t --new                New log file.")
    print("\t --force              No ask for dangerous operations.")
    print("\t --help , -h          Print this help message.")
    print("\t --info               Print info about this program.")
    print("\t --csv-dump --print|<filename>   Dump logs into CSV (raw data). \"--print\" for print on screen.")
    print("\n")
    exit()


if __name__ == "__main__":
    filename = False
    where = False
    operation = False
    force = False
    i = 1
    while i < len(argv):
        if argv[i] == "-f":
            try:
                filename = argv[i+1]
            except:
                print_exit("Missing filename:  -f <filename>")
            i += 1
        elif argv[i] == "--add" and not operation:
            operation = 1
            try:
                text = argv[i+1]
            except:
                print_exit("Missing text:  --add <text>")
            i += 1
        elif argv[i] == "--where":
            try:
                where = argv[i+1]
            except:
                print_exit("Missing where condition:  --where <conditions>")
            i += 1
        elif argv[i] == "--query" and not operation:
            operation = 4
            try:
                query = argv[i+1]
            except:
                print_exit("Missing query:  --query <query>")
            i += 1
        elif argv[i] == "--show" and not operation:
            operation = 5
        elif argv[i] == "--verify-integrity" and not operation:
            operation = 2
        elif argv[i] == "--new" and not operation:
            operation = 3
        elif argv[i] == "--csv-dump" and not operation:
            operation = 6
            try:
                csvDumpArg = argv[i+1]
            except:
                print_exit("Missing CSV destination:  --csv-dump --print|<filename>")
            i += 1
        elif argv[i] == "--force":
            force = True
        elif argv[i] == "--info":
            print_info()
        elif argv[i] == "-h" or argv[i] == "--help":
            print_help()
        else:
            print("Invalid arguments:  \"" + argv[i] + "\"")
            print_help()
        i += 1
    if not filename:
        print_exit("Missing filename:  -f <filename>")
    if not operation:
        print_exit("Missing operation. See help message or documentation.")
    try:
        conn = sqlite3.connect(filename)
        c = conn.cursor()
    except:
        print_exit("Error on opening sqlite3 connection.")
    
    if operation == 1:
        # New record
        try:
            c.execute("SELECT hash FROM logs ORDER BY time DESC LIMIT 1;")
            lastHash = c.fetchall()[0][0]
            timestamp = int(time())
            currentHash = sha256(lastHash + str(timestamp) + text).hexdigest()
            c.execute("INSERT INTO logs (time, message, hash) VALUES (?, ?, ?) ;", (timestamp, text, currentHash))
            conn.commit()
        except:
            print_exit("Query Error. Impossible insert new record.")
    
    elif operation == 2:
        # Check integrity
        try:
            c.execute("SELECT time, message, hash FROM logs;")
            records = c.fetchall()
            i = 1
            while i < len(records):
                if not sha256(records[i-1][2] + str(records[i][0]) + records[i][1]).hexdigest() == records[i][2]:
                    print("Integrity violated in row " + str(i+1) + ":")
                    print(str(i) + " : " + datetime.utcfromtimestamp(records[i-1][0]).strftime('%Y-%m-%d %H:%M:%S') + "\t" + records[i-1][1] + "\t" + records[i-1][2])
                    print(str(i+1) + " : " + datetime.utcfromtimestamp(records[i][0]).strftime('%Y-%m-%d %H:%M:%S') + "\t" + records[i][1] + "\t" + records[i][2])
                    exit()
                i += 1
            print_exit("Integrity verified. No errors in " + str(i) + " records.")
        except Exception as exc:
            print_exit("Query Error: " + str(exc))
    
    elif operation == 3:
        # Create new log file
        try:
            c.execute("CREATE TABLE logs (time INT, message TEXT, hash TEXT);")
            conn.commit()
            c.execute("INSERT INTO logs (time, message, hash) VALUES (?, 'Create log file.', ?) ;", (int(time()), sha256(str(random())).hexdigest()))
            conn.commit()
        except:
            print_exit("Query Error. Impossible create new table. 'logs' table may be already exists.")
    
    elif operation == 4:
        # Custom query
        if not force:
            answer = raw_input("Are you sure to execute this query? \"yes\"/\"no\" : ")
            if answer == "no":
                print_exit("Operation Canceled.")
            elif not answer == "yes":
                print_exit("Invalid Answer. Operation Canceled.")
        try:
            c.execute(query)
            conn.commit()
        except Exception as exc:
            print_exit("Query Error. Impossible execute this query: " + str(exc))
    
    elif operation == 5:
        # Show logs
        query = "SELECT time, message FROM logs"
        if where:
            query += " WHERE " + where + ";"
        else:
            query += ";"
        try:
            c.execute(query)
            records = c.fetchall()
            for record in records:
                print(datetime.utcfromtimestamp(record[0]).strftime('%Y-%m-%d %H:%M:%S') + "\t\t" + record[1])
        except Exception as exc:
            print_exit("Query Error: " + str(exc))
    
    elif operation == 6:
        # Create CSV dump
        query = "SELECT time, message, hash FROM logs"
        if where:
            query += " WHERE " + where + ";"
        else:
            query += ";"
        try:
            c.execute(query)
            records = c.fetchall()
            csvData = ""
            for record in records:
                csvData += str(record[0]) + ";" + record[1] + ";" + record[2] + "\n"
            if csvDumpArg == "--print":
                print(csvData)
            else:
                try:
                    fp = open(csvDumpArg, "w")
                    fp.write(csvData)
                    fp.close()
                except:
                    print_exit("Error I/O on \"" + csvDumpArg + "\"")
        except Exception as exc:
            print_exit("Query Error: " + str(exc))
    
    try:
        conn.close()
    except:
        print_exit("Error on closing sqlite3 connection.")

