import demjson

def parse_json(input_text, delimeters):
    input_text = input_text.strip()
    formatted_text = replace_strings(input_text, delimeters)
    return demjson.decode(formatted_text)


def replace_strings(input_text, delimeters):
    for delimeter in delimeters:
        status = True
        while status:
            try:
                start_index = input_text.rindex(delimeter)
                end_index = start_index + input_text[start_index:].find(",") + 1
                replacing_string = input_text[start_index:end_index]
                input_text = input_text.replace(replacing_string, "")
            except ValueError:
                status = False
    input_text = input_text.replace("=", ":").replace(";", "")
    formatted_text = "{" + input_text + "}"
    return formatted_text