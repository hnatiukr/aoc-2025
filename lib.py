def read_input(input_filename: str, joined=False):
    buffer = open(input_filename, "r")
    input_map = map(lambda x: x.replace("\n", ""), buffer.readlines())
    input_list = list(input_map)
    if joined:
        return "".join(input_list)
    return input_list
