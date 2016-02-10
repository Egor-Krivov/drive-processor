def process(path_in, path_out):
    with open(path_in, 'rb') as input, open(path_out, 'wb') as output:
        for line in input:
            output.write(line)
