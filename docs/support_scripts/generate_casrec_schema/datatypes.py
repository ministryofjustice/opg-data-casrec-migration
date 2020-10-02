import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

casrec_codes = ["700C","3C","8UA","2UB","8C","25C","28C","40C","15C","2UA","30C","4C","1C","1UB","2C","6UA","4UA","9C","5C","20C","16C","7C","7UA","10C","13C","64C","440C","1UA","3UA","38C","100C","6C","810C","11C","60C","35C","500C","220C","23C","180C","83C","50C","58C","400C","19C","10UA","24C","600C","145C","1600C","108C","950C","18C","4UB","3UB","12C","10SA","22C","620C","14UA","17C","560C","65C","686C","170C","120C","34C","374C","105C","32C","169C","720C","699C","86C","375C","350C","44C","300C","57C","1100C","1000C","54C","880C","70C","200C","6SA","8SB","420C","8UB","450C","27C","48C","250C","150C","8SP","5UB","42C","240C","31C","4SA","80C","21C","74C","3100C","3000C","77C","140C","29C","33C","110C","1060C","460C","36C","2SB","1406C","1106C","61C","1200C","69C","14C","75C","900C","46C","800C","5UA",]


mapping = pd.DataFrame()

for code in casrec_codes:
    code_details = {}
    code_details['code'] = code

    if code == '1C':
        code_details['pg_datatype'] = "varchar(1)"
        code_details['field_type'] = "boolean"
        code_details['field_format'] = ""
        code_details['char_limit'] = '1'
        code_details['details'] = "Boolean string"

    elif 'C' in code:
        length = code[:code.index('C')]
        code_details['pg_datatype'] = f"varchar({length})"
        code_details['field_type'] = "text"
        code_details['field_format'] = ""
        code_details['char_limit'] = length
        code_details['details'] = f"Normal string with char limit {length}"

    elif 'UBE' in code:

        length = code[:code.index('UBE')]
        code_details['pg_datatype'] = "int"
        code_details['char_limit'] = length
        code_details['field_type'] = "int"
        code_details['field_format'] = ""
        code_details['details'] = f"int with limit {length}"

    elif code == '8UA':
        code_details['pg_datatype'] = f"varchar(8)"
        code_details['char_limit'] = '8'
        code_details['field_type'] = "date"
        code_details['field_format'] = 'YYYYMMDD'
        code_details['details'] = f"date with format YYYYMMDD"

    elif code in ['6UA']:
        code_details['pg_datatype'] = f"varchar(8)"
        code_details['char_limit'] = '8'
        code_details['field_type'] = "text"
        code_details['field_format'] = "DDMMYY"
        code_details['details'] = f"date with format DDMMYY or HHMMSS"


    elif 'UB' in code:
        length = code[:code.index('UB')]
        code_details['pg_datatype'] = f"varchar({length})"
        code_details['char_limit'] = length

        if code in ['2UBE', '2BE']:
            code_details['details'] = f"time? notes say 'Two-secs'"
            code_details['field_type'] = "time"
            code_details['field_format'] = ""

        elif code in ['3UBE', '3UB']:
            code_details['details'] = f"time with format HHMMSS?"
            code_details['field_type'] = "time"
            code_details['field_format'] = "HHMMSS"

        elif code == '5UBE':
            code_details['details'] = f"date with format YYYYNNN (day number)"
            code_details['field_type'] = "date"
            code_details['field_format'] = "YYYYNNN"

        else:
            code_details['details'] = "Unknown"
            code_details['field_type'] = "text"
            code_details['field_format'] = ""




    elif 'UA' in code:
        length = code[:code.index('UA')]
        code_details['pg_datatype'] = f"varchar({length})"
        code_details['char_limit'] = length
        code_details['field_type'] = "text"
        code_details['field_format'] = ""
        code_details['details'] = f"String with char limit " \
                                  f"{length}, sometimes a date or " \
                                  f"time, sometimes maybe a lookup?"

    elif 'SA' in code:
        length = code[:code.index('SA')]
        code_details['pg_datatype'] = f"varchar({length})"
        code_details['char_limit'] = length
        code_details['field_type'] = "money"
        code_details['field_format'] = ""
        code_details['details'] = f"Looks like money with char limit" \
                                  f" {length}"

    elif code in ['8SBE', '8SPD', '8SB', '8SP']:
        code_details['pg_datatype'] = "varchar(8)"
        code_details['char_limit'] = '8'
        code_details['field_type'] = "money"
        code_details['field_format'] = ""
        code_details['details'] = "Looks like money with char limit of 8"

    elif code in ['2SB']:
        code_details['pg_datatype'] = "int"
        code_details['char_limit'] = '2'
        code_details['field_type'] = "int"
        code_details['field_format'] = ""
        code_details['details'] = "Count? Char limit 2"

    else:
        code_details['pg_datatype'] = ""
        code_details['char_limit'] = ''
        code_details['field_type'] = ""
        code_details['field_format'] = ""
        code_details['details'] = "Mystery"


    mapping = mapping.append(code_details, ignore_index=True)


print(mapping)
# print(mapping[mapping['pg_datatype'].isnull()])
