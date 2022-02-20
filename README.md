# Gmail Tools

Search for and batch forward Gmail messages.

## Installation

The code is available on [GitHub](https://github.com/JimmyVanHout/gmail_tools). Note that `gmail_search.py` **does write to files** so you may want to save this file to its own directory.

## Search

### Usage

Run:

```
python3 gmail_search.py <query_str> [--use-config-file] [--save-messages]
```

The query string `<query_str>` must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4).

`--use-config-file` attempts to load configuration data--email address, password, mailbox, and whether to clean message data (see below)--from `config.txt` so that it doesn't have to be entered each time. If it cannot find the file, the user will be asked for input and the file will be created with this configuration data. Note that the password is stored **unencrypted** in the configuration file.

`--save-messages` saves the retrieved messages to a directory `messages`. The default is to print the messages to standard output.

When running the program, the user will be asked to enter their email address, password, mailbox (the default is `inbox`), and whether messages should be cleaned to remove `=\r\n` strings that Gmail adds.

#### Example

```
python3 gmail_search.py "FROM email@email.com" --use-config-file --save-messages
```

## Batch Forward

### Usage

Run:

```
python3 gmail_batch_forward.py
```

When running the program, the user will be asked to enter the originating email address, its password, the receiving email addresses, the query string, and the mailbox to search in (the default is `inbox`). Note that the query string must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4).

#### Example

```
$ python3 gmail_batch_forward.py
Originating email address: email@email.com
Password: mypassword
Receiving email addresses (comma-separated): email1@email.org, email2@email.com
Query string: FROM email3@email.net
Mailbox to search in (left blank, default is "inbox"):
```
