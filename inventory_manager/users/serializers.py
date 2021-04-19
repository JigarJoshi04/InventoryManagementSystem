import json

def convert_bytes_array_to_json(bytes_string):
    converted_json = bytes_string.decode('utf8').replace("'", '"')
    data = json.loads(converted_json)
    return data
    # s = json.dumps(data)
    # print(s)