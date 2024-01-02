
# Hash Chain Logging System (python alpha 0.1)

### - Problems of Common Logging Systems

The logging systems have the simple function of tracking events in the past by marking for each event a timestamp and some informations (in the simplest case a simple string).
The log mark events of the past and therefore should not be changed (the past does not change).
Sometimes logging systems mark important events such as access to sensitive systems, conversations and a lot of sensitive information... and unfortunately these informations can easily be corrupted/changed in most cases.
**Hash Chain Logging System** is one of many approaches that can be used to prevent data corruption, or the more specific, recognize what data has been manipulated or not.
This approach is not anything new and it's the primary mechanism used by blockchain to be secure and verifiable: the use of recursive hashes.

Its features are:
- Create new file log (sqlite3 format)
- Add new logs
- Automatic verify integrity
- Free SQL query
- Print formatted data and CSV export with custom WHERE conditions


### - Basic Use of python-hash-chain-logging-system

For create new file named "history.log" type

```
$ hash-chain-logging-system -f history.log --new
```

For add new log into "history.log"

```
$ hash-chain-logging-system -f history.log --add 'Text to insert.'
```

For print all formatted logs into "history.log"

```
$ hash-chain-logging-system -f history.log --show
2019-02-25 10:29:22		Create log file.
2019-02-25 10:30:45		Text to insert.
2019-02-25 10:32:38		Another Text.
2019-02-25 10:32:49		Hello, World!
2019-02-25 10:33:16		Random Message

```

For verify integrity into "history.log"

```
$ hash-chain-logging-system -f history.log --verify-integrity
Integrity verified. No errors in 5 records.
```

In case of corruption:

```
$ hash-chain-logging-system -f history.log --query 'UPDATE logs SET message = "Hello!" WHERE message = "Hello, World!";' --force
$ hash-chain-logging-system -f history.log --verify-integrity
Integrity violated in row 4:
3 : 2019-02-25 10:32:38	Another Text.  0a883aaed02a53180a8f07b3f837ad874c8074d21a8fff80ef3e0df1b26cc7f2
4 : 2019-02-25 10:32:49	Hello!	cb2b6962f3fcc56de8d5f8c81d0bfbdbf669f8cf73792d38180864165dac5635

```


### - Installation and Uninstallation

For install python-hash-chain-logging-system follow these steps:

```
$ git clone https://github.com/Gorresio/python-hash-chain-logging-system
$ cd python-hash-chain-logging-system
```

Compile it (from here on **python** is required)

```
$ ./compile
```

And how root install it

```
# ./install
```

For uninstall

```
# ./uninstall
```

If install and uninstall script generate error how *Permission Denied* or *./install: command not found*, Make sure that of correct permission and if the scripts are marked as executable.

If not, type:

```
$ chmod +x compile install uninstall
```

### - Structure

Log files are sqlite3 database with single table with following structure

```
logs (
    time INT,
    message TEXT,
    hash TEXT
)
```

The time is saved how **POSIX UTC timestamp**.
Informations into each record are stored into single ASCII text.
Hash function is **sha256** and it's defined:

```
currentHash = sha256(lastHash + str(timestamp) + text).hexdigest()
```

As you can see, the system does not aim at maximum efficiency, but at the simplicity of exporting and reading.
### - Note

hash-chain-logging-system is a free software licensed by Simplified BSD License.

Copy of Simplified BSD License license is present in ./LICENSE file

If you notice any violations by myself or by third parties, please contact me.

The use of hash-chain-logging-system is at your own risk: read thelicense.

Stefano Gorresio

Email: stefano.gorresio@gmail.com

