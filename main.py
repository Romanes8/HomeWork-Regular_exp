import re
import csv


#функция сортировки имени, фамилии, отчества по графам 'lastname', 'firstname', 'surname'
def sort_name(contacts_list):
    con_list = contacts_list
    con_list.pop(0)
    presorted_con_list = con_list
    list_lastname = []
    list_firstname = []
    list_surname = []
    for el in presorted_con_list:
        lastname_el = el[0].split(' ')
        firstname_el = el[1].split(' ')
        surname_el = el[2].split(' ')
        list_lastname.append(lastname_el[:3])
        list_firstname.append(firstname_el[:3])
        list_surname.append(surname_el[:3])

    name_list = [x + y + z for x, y, z in zip(list_lastname, list_firstname, list_surname)]
    for lists in name_list:
        for elem in lists:
            if elem == '':
                lists.remove(elem)

    sorted_con_list = []
    for elms, el in zip(presorted_con_list, name_list):
        elms[0] = el[0]
        elms[1] = el[1]
        elms[2] = el[2]
        sorted_con_list.append(elms)
    return sorted_con_list


# функция форматирования номеров телефонов
def format_phone_number(contacts_list, pattern, subst_pattern):
    format_phone_list = []
    count = 0
    for i in contacts_list:
        string = (',').join(contacts_list[count])
        count += 1
        pattern_ = re.compile(pattern)
        result = pattern_.sub(subst_pattern, string)
        string_list = result.split(',')
        format_phone_list.append(string_list)
    return format_phone_list


# функция объединения дублирующихся контактов
def join_double(contacts_list):
    for contact in contacts_list:
        last_name = contact[0]
        first_name = contact[1]
        for new_contact in contacts_list:
            new_last_name = new_contact[0]
            new_first_name = new_contact[1]
            if first_name == new_first_name and last_name == new_last_name:
                if contact[2] == '':
                    contact[2] = new_contact[2]
                if contact[3] == '':
                    contact[3] = new_contact[3]
                if contact[4] == '':
                    contact[4] = new_contact[4]
                if contact[5] == '':
                    contact[5] = new_contact[5]
                if contact[6] == '':
                    contact[6] = new_contact[6]
    result_list = [['lastname', 'firstname', 'surname', 'organization', 'position', 'phone,email']]
    for i in contacts_list:
        if i not in result_list:
            result_list.append(i)
    return result_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

        # вызов функции сортировки имени, фамилии, отчества по графам 'lastname', 'firstname', 'surname'
        sorted_con_list = sort_name(contacts_list)

        # задание параметров и вызов функции форматирования номеров телефонов
        pattern = r'(\+7|8)\s*\(*(\d+)\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(*(\w+\.*\s*\d+)*\)*'
        subst_pattern = r'8(\2)\3-\4-\5 \6'
        format_phone_list = format_phone_number(sorted_con_list, pattern, subst_pattern)

        # вызов функции объединения дублирующихся контактов
        result_list = join_double(format_phone_list)


    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_list)
        print('Файл "phonebook.csv" создан.')
