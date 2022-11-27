import csv
import re


with open("phonebook_raw.csv") as f:
    f.readline()
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    clients = {}
    temp = {}
    for lastname, firstname, surname, organization, position, phone, *email in contacts_list:
        pattern1 = re.compile(r"\+?[7|8]?\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})\s\(?доб.\s(\d{"
                              r"4})\)?")
        pattern2 = re.compile(r"\+?[8|7]?\s?\(?(\d{3})\)?\s?\-?(\d{3})\-?\s?(\d{2})\s?\-?(\d{2})")
        if "доб." not in phone:
            phone = pattern2.sub(r"+7(\1)\2-\3-\4", phone)
        else:
            phone = pattern1.sub(r"+7(\1)\2-\3-\4 доб.\5", phone)
        client = (lastname + ' ' + firstname + ' ' + surname).split(' ')
        if client[0] not in clients:
            temp = {'lastname': client[0], 'firstname': client[1], 'surname': client[2], "organization": organization,
                    "position": position, "phone": phone, "email": email[0]}
            clients[client[0]] = temp
        else:
            if clients[client[0]]["lastname"] == "":
                clients[client[0]]["lastname"] = clients[client[0]]["lastname"] + client[0]
            if clients[client[0]]["firstname"] == "":
                clients[client[0]]["firstname"] = clients[client[0]]["firstname"] + client[1]
            if clients[client[0]]["surname"] == "":
                clients[client[0]]["surname"] = clients[client[0]]["surname"] + client[2]
            if clients[client[0]]["organization"] == "":
                clients[client[0]]["organization"] = clients[client[0]]["organization"] + organization
            if clients[client[0]]["position"] == "":
                clients[client[0]]["position"] = clients[client[0]]["position"] + position
            if clients[client[0]]["phone"] == "":
                clients[client[0]]["phone"] = clients[client[0]]["phone"] + phone
            if clients[client[0]]["email"] == "":
                clients[client[0]]["email"] = clients[client[0]]["email"] + email[0]
    print(*clients)


with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerow(["lastname", "firstname", "surname", "organization", "position", "phone", "email"])
    for rows in clients.values():
        datawriter.writerow(rows.values())

# пример регулярки для телефонов: (8|+7)?\s((\d+))\s(\d+)[-\s](\d{2})[-\s](\d{2})
# пример шаблона для форматирования телефона: +7-\2-\3-\4-\5
