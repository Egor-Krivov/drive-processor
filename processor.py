def process(file_in, file_out):
    with open(file_in, 'rb') as input, open(file_out, 'wb') as output:
        for line in input:
            print('text')
            output.write(line)
