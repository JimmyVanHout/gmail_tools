# Gmail Search

Search for and retrieve Gmail messages.

## Installation

Download the file `gmail_search.py`. Note that this program **does write to files** so you may want to save this file to a new directory.

## Usage

Run:

```
python3 gmail_search.py <query_str> [--use-config-file] [--save-messages]
```

The query string `<query_str>` must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4).

`--use-config-file` attempts to load configuration data--email address, password, mailbox, and whether to clean message data (see below)--from `config.txt` so that it doesn't have to be entered each time. If it cannot find the file, the user will be asked for input and the file will be created with this configuration data. Note that the password is stored **unencrypted** in the configuration file.

`--save-messages` saves the retrieved messages to a directory `messages`. The default is to print the messages to stdout.

When running the program, the user will be asked to enter their email address, password, mailbox (the default is `inbox`), and whether messages should be cleaned to remove `=\r\n` strings that Gmail adds.

### Example

```
python3 gmail_search.py "FROM email@email.com" --use-config-file --save-messages
```
