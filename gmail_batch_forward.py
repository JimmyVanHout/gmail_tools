import getpass
import gmail_search
import imaplib
import random
import re
import smtplib
import ssl
import sys
import time

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = "993"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "465"
LOWER_BOUND_RANDRANGE = 1
UPPER_BOUND_PLUS_ONE_RANDRANGE = 5

def send(email_address, password, receiving_email_addresses, messages):
    smtpssl = setup(email_address, password)
    print("Forwarding messages")
    count = 1
    for receiving_email_address in receiving_email_addresses:
        for message in messages:
            smtpssl.sendmail(email_address, receiving_email_address, message)
            print("Progress: {percentage:.2f}%".format(percentage=(count / len(messages) * len(receiving_email_addresses) * 100)))
            count += 1
            delay = random.randrange(LOWER_BOUND_RANDRANGE, UPPER_BOUND_PLUS_ONE_RANDRANGE)
            time.sleep(delay)
    smtpssl.quit()
    print("Finished forwarding all mail")

def setup(email_address, password):
    ssl_context = ssl.create_default_context()
    smtpssl = smtplib.SMTP_SSL(host=SMTP_SERVER, port=SMTP_PORT, context=ssl_context)
    smtpssl.login(email_address, password)
    return smtpssl

def get_subjects(messages):
    subjects = []
    for message in messages:
        subject_pattern = re.compile(r"(Subject\: .*?)\r?\n")
        subject = re.search(subject_pattern, message).group(1)
        subjects.append(subject)
    return subjects

def shorten_messages(messages):
    shortened_messages = []
    for message in messages:
        message = message[message.find("Content-Type: "):]
        shortened_messages.append(message)
    return shortened_messages

def add_subjects(messages, subjects):
    subjects_with_messages = []
    for i in range(len(messages)):
        message = subjects[i] + "\n" + messages[i]
        subjects_with_messages.append(message)
    return subjects_with_messages

def print_correct_usage():
    print("Correct usage:\n")
    print("python3 gmail_batch_forward.py")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_correct_usage()
        sys.exit(1)
    email_address = input("Originating email address: ")
    password = getpass.getpass("Password: ")
    receiving_email_addresses_input = input("Receiving email addresses (comma-separated): ")
    receiving_email_addresses = [rea.strip() for rea in receiving_email_addresses_input.split(",")]
    search_str = input("Query string: ")
    mailbox = input("Mailbox to search in (left blank, default is \"inbox\"): ")
    if mailbox == "":
        mailbox = "inbox"
    messages = gmail_search.search(email_address, password, search_str, mailbox)
    subjects = get_subjects(messages)
    messages = shorten_messages(messages)
    messages = add_subjects(messages, subjects)
    send(email_address, password, receiving_email_addresses, messages)
    sys.exit(0)
