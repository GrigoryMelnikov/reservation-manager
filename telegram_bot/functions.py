import phonenumbers


def phone_validation(phone_num) -> list:
    try:
        phone_num = phone_num.replace('-', '').replace(' ', '').strip()
        if phone_num[0] == '0':
            phone_num = phone_num.replace("0", "+972", 1)
        elif phone_num[0] != '+':
            phone_num = '+' + phone_num
        parsed_num = phonenumbers.parse(phone_num)
        bul_vali = phonenumbers.is_valid_number(parsed_num)
    except:
        bul_vali = False
    return [phone_num, bul_vali]