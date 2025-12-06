def read_input_lines(input_filename: str) -> list[str]:
    buffer = open(input_filename, "r")
    input_map = map(lambda x: x.replace("\n", ""), buffer.readlines())
    input_list = list(input_map)

    return input_list
