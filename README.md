# Gmail Search

Search from and retrieve Gmail messages.

## Installation

Download the file `gmail_search.py`.

## Usage

Run:

```
python3 gmail_search.py [--use-config-file] [--save-messages]
```

`--use-config-file` specifies to save user input in a file `config.txt` so that it doesn't have to be entered each time.

`--save-messages` saves the retrieved messages to a directory `messages`. The default is to print the messages to stdout.

When running the program, the user will be asked to enter their email address, password, query string (must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4)), mailbox (the default is `inbox`), and whether messages should be cleaned to remove `=\r\n` strings that Gmail adds.
