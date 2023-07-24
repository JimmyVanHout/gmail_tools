# Gmail Tools

Search for and batch forward Gmail messages, and extract PDFs from Gmail messages.

## Installation

Install the code from [GitHub](https://github.com/JimmyVanHout/gmail_tools):

```
git clone https://github.com/JimmyVanHout/gmail_tools.git
```

Note that `gmail_search.py` and `gmail_extract_pdfs.py` **do write to files** so ensure that they are contained in their own directory (such as the repository directory).

## Gmail Account Configuration

In order for the programs to access your Gmail account, you must create an [application-specific password](https://support.google.com/mail/answer/185833?hl=en-GB) and use this password when running these programs.

## Search

### Usage

Run:

```
python3 gmail_search.py <query_str> [--use-config-file] [--save-messages]
```

The query string `<query_str>` must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4).

`--use-config-file` attempts to load configuration data--email address, password, and mailbox--from `config.txt` so that it doesn't have to be entered each time. If it cannot find the file, the user will be asked for input and the file will be created with this configuration data. Note that the password is stored **unencrypted** in the configuration file. Also note that, if not specified, the default mailbox is `inbox`.

`--save-messages` saves the retrieved messages to a directory `messages`. The default is to print the messages to standard output.

When running the program, the user will be asked to enter their email address, password, and mailbox (the default is `inbox`).

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

Also, although it worked for multiple email formats in limited testing, the batch send functionality was designed for a specific email format and therefore may not work for every email one may attempt to forward.

#### Example

```
$ python3 gmail_batch_forward.py
Originating email address: email@email.com
Password: mypassword
Receiving email addresses (comma-separated): email1@email.org, email2@email.com
Query string: FROM email3@email.net
Mailbox to search in (left blank, default is "inbox"):
```

## Extract PDFs

### Usage

Run:

```
python3 gmail_extract_pdfs.py <query_str> <beginning_of_name> [--use-config-file]
```

`--use-config-file` attempts to load configuration data--email address, password, and mailbox--from `config.txt` so that it doesn't have to be entered each time. If it cannot find the file, the user will be asked for input and the file will be created with this configuration data. Note that the password is stored **unencrypted** in the configuration file. Also note that, if not specified, the default mailbox is `inbox`.

The program uses the query string `<query_str>` to search the target Gmail account and extracts a maximum of one PDF attachment from each email that matches the search query. The query string `<query_str>` must be formatted according to [RFC 3501 6.4.4](https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4). `<beginning_of_name>` specifies the beginning of the filename that each PDF will take on. The filename of each PDF will continue with a hyphen and the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)-formatted timestamp of when the email was received. For example, if `<beginning_of_name>` is specified as `myfilename` and two emails with PDFs were found, received on November 12, 2021 at 10:22:36 and January 18, 2022 at 18:12:01, respectively, then the PDFs would be saved as `myfilename-2021-11-12T10-22-36` and `myfilename-2022-01-18T18-12-01`. The PDFs are saved in a directory `pdfs`.

### Example

```
python3 gmail_extract_pdfs.py "FROM email@email.com" mypdf --use-config-file
```
