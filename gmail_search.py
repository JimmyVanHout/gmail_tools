import imaplib
import os
import ssl
import sys

VALID_OPTIONS = ["--use-config-file", "--save-messages"]
CONFIG_FILE_NAME = "config.txt"
IMAP_SERVER = "imap.gmail.com"
PORT = "993"

def search(email_address, password, search_str, mailbox="inbox", clean_messages=True):
    imap4ssl = setup(email_address, password, mailbox)
    message_ids = get_message_ids(imap4ssl, search_str)
    messages = get_messages(imap4ssl, message_ids)
    if clean_messages:
        messages = clean(messages)
    finish(imap4ssl)
    return messages

def setup(email_address, password, mailbox):
    ssl_context = ssl.create_default_context()
    imap4ssl = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=PORT, ssl_context=ssl_context)
    imap4ssl.login(email_address, password)
    imap4ssl.select(mailbox)
    return imap4ssl

def get_message_ids(imap4ssl, search_str):
    message_ids = imap4ssl.search(None, search_str)[1][0].split()
    print("Found " + str(len(message_ids)) + " messages")
    return message_ids

def get_messages(imap4ssl, message_ids):
    messages = []
    print("Fetching messages")
    count = 1
    for message_id in message_ids:
        message = imap4ssl.fetch(message_id, "(RFC822)")[1][0][1].decode("utf-8")
        messages.append(message)
        print("Progress: {percentage:.2f}%".format(percentage=(count / len(message_ids) * 100)))
        count += 1
    print("Finished fetching messages")
    return messages

def clean(messages):
    cleaned_messages = []
    for message in messages:
        cleaned_message = message.replace("=\r\n", "")
        cleaned_messages.append(cleaned_message)
    return cleaned_messages

def finish(imap4ssl):
    imap4ssl.close()
    imap4ssl.logout()

def print_correct_usage():
    print("Correct use:\n")
    print("python3 gmail_search.py <query_str> [--use_config_file] [--save_messages]")

def get_config_data_from_input():
    email_address = input("Email address: ")
    password = input("Password: ")
    mailbox = input("Mailbox (default is \"inbox\"): ")
    clean_messages = input("Remove unnecessary characters from messages (yes or no)?: ")
    if mailbox == "":
        mailbox = "inbox"
    return email_address, password, mailbox, clean_messages

def write_data_to_config_file(email_address, password, mailbox, clean_messages):
    with open(CONFIG_FILE_NAME, "w") as file:
        file.write(email_address + " # email address\n")
        file.write(password + " # password\n")
        file.write(mailbox + " # mailbox\n")
        file.write(clean_messages + " # Clean messages?\n")

def read_data_from_config_file():
    with open(CONFIG_FILE_NAME, "r") as file:
        email_address = file.readline().split("#", 1)[0].rstrip()
        password = file.readline().split("#", 1)[0].rstrip()
        mailbox = file.readline().split("#", 1)[0].rstrip()
        clean_messages_input = file.readline().split("#", 1)[0].rstrip()
        clean_messages = True if clean_messages_input == "yes" or clean_messages_input == "y" else False
        return email_address, password, mailbox, clean_messages

def write_messages_to_files(messages):
    for i in range(len(messages)):
        with open("message_" + str(i + 1) + ".txt", "w") as file:
            file.write(messages[i])

def print_messages(messages):
    for message in messages:
        print(message)

def is_command_valid(command):
    if len(command) == 1:
        return False
    for word in command[2:]:
        if word not in VALID_OPTIONS:
            return False
    return True

if __name__ == "__main__":
    command = sys.argv[sys.argv.index("gmail_search.py"):]
    if not is_command_valid(command):
        print_correct_usage()
        sys.exit(1)
    search_str = command[1]
    use_config_file = True if "--use-config-file" in command else False
    save_messages = True if "--save-messages" in command else False
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    email_address = password = mailbox = clean_messages = None
    if use_config_file:
        if CONFIG_FILE_NAME in os.listdir():
            email_address, password, mailbox, clean_messages = read_data_from_config_file()
        else:
            email_address, password, mailbox, clean_messages = get_config_data_from_input()
            write_data_to_config_file(email_address, password, mailbox, clean_messages)
    else:
        email_address, password, mailbox, clean_messages = get_config_data_from_input()
    messages = search(email_address, password, search_str, mailbox, clean_messages)
    if save_messages:
        if not os.path.isdir("messages"):
            os.mkdir("messages")
        os.chdir("messages")
        write_messages_to_files(messages)
        os.chdir("..")
    else:
        print_messages(messages)
    sys.exit(0)
