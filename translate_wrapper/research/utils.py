def read_from_file(filename: str):
    result = ''
    with open(filename) as f:
        for line in f:
            result += line
    return result
