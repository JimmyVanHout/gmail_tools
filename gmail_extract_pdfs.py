import datetime
import email
import getpass
import gmail_search
import os
import re
import sys

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = "993"
VALID_OPTIONS = ["--use-config-file"]
CONFIG_FILE_NAME = "config.txt"

def get_dates_and_pdfs(messages):
    dates_and_pdfs = []
    for message in messages:
        pdf = None
        message_obj = email.message_from_string(message)
        for part in message_obj.get_payload():
            if part.get_content_type() == "application/octet-stream":
                pdf = part.get_payload(decode=True)
                break
        date_pattern = re.compile(r"Date\: (?P<day_of_week>\w+), (?P<day>\d+) (?P<month>\w+) (?P<year>\d+) (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)")
        date_match_groups = re.search(date_pattern, message).groupdict()
        date = datetime.datetime.strptime(" ".join(list(date_match_groups.values())), "%a %d %b %Y %H %M %S")
        dates_and_pdfs.append((date, pdf))
    return dates_and_pdfs

def write_pdfs(dates_and_pdfs, beginning_of_name):
    for date, pdf in dates_and_pdfs:
        name = beginning_of_name + "-" + date.isoformat().replace(":", "-") + ".pdf"
        with open(name, "wb") as file:
            file.write(pdf)

def get_config_data_from_input():
    email_address = input("Email address: ")
    password = getpass.getpass("Password: ")
    mailbox = input("Mailbox (default is \"inbox\"): ")
    if mailbox == "":
        mailbox = "inbox"
    return email_address, password, mailbox

def write_data_to_config_file(email_address, password, mailbox):
    with open(CONFIG_FILE_NAME, "w") as file:
        file.write(email_address + " # email address\n")
        file.write(password + " # password\n")
        file.write(mailbox + " # mailbox\n")

def read_data_from_config_file():
    with open(CONFIG_FILE_NAME, "r") as file:
        email_address = file.readline().split("#", 1)[0].rstrip()
        password = file.readline().split("#", 1)[0].rstrip()
        mailbox = file.readline().split("#", 1)[0].rstrip()
        return email_address, password, mailbox

def print_correct_usage():
    print("Correct use:\n")
    print("python3 gmail_extract_pdfs.py <query_str> <beginning_of_name> [--use_config_file]")

def is_command_valid(command):
    if len(command) < 3:
        return False
    if len(command) > 3:
        for word in command[3:]:
            if word not in VALID_OPTIONS:
                return False
    return True

def get_command_start_index(args):
    for i in range(len(args)):
        if os.path.basename(os.path.realpath(__file__)) in sys.argv[i]:
            return i

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    command = sys.argv[get_command_start_index(sys.argv):]
    if not is_command_valid(command):
        print_correct_usage()
        sys.exit(1)
    search_str = command[1]
    beginning_of_name = command[2]
    use_config_file = True if "--use-config-file" in command else False
    if use_config_file:
        if CONFIG_FILE_NAME in os.listdir():
            email_address, password, mailbox = read_data_from_config_file()
        else:
            email_address, password, mailbox = get_config_data_from_input()
            write_data_to_config_file(email_address, password, mailbox)
    else:
        email_address, password, mailbox = get_config_data_from_input()
    messages = gmail_search.search(email_address, password, search_str, mailbox)
    dates_and_pdfs = get_dates_and_pdfs(messages)
    if not os.path.isdir("pdfs"):
        os.mkdir("pdfs")
    os.chdir("pdfs")
    write_pdfs(dates_and_pdfs, beginning_of_name)
    os.chdir("..")
    sys.exit(0)
