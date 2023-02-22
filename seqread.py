import os
import sys


def readportion_block(file, start, end, block_size=10000):
    """do a blockwise read"""
    file.seek(start)
    while file.tell() < end:
        if (end - file.tell() < block_size) or (file.tell() + block_size >= end):
            return file.read(end - file.tell())
        else:
            block = file.read(block_size)
            yield block

def readportion(file, start, end, block_size=10000):
    """do a raw read"""
    file.seek(start)
    return file.read(end - start)

def read_large_file(file_handler, block_size=10000):
    block = []
    for line in file_handler:
        block.append(line)
        if len(block) == block_size:
            yield block
            block = []

    # don't forget to yield the last block
    if block:
        yield block


def getparm(name, default=None):
    try:
        if name in sys.argv:
            return sys.argv[sys.argv.index(name) + 1]
    except:
        pass
    return default

def print_usage():
    print('Usage: seqread.py filename -s <int> -e <int>')
    print('   -h or --help for this help message')
    print('   -s start byte (default 0)')
    print('   -e end byte (default file length)')
    print('   -l length (default file length)')
    sys.exit(0)

def command_line_parameters():
    """Deal with command line parameters"""
    global start, end, length, reported_length

    if len(sys.argv) < 2:
        # user did not specify a filename
        print('ERROR: You must specify a filename')
        print_usage()


    # if the user specified help, print it and exit
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_usage()

    # if the user specified a start, use it
    start = int(getparm('-s', 0))

    # see if file exists and get its reported_length
    try:
        reported_length = os.path.getsize(sys.argv[1])
    except:
        print('File not found')
        sys.exit(1)

    # if the user specified an end, use it   
    end = int(getparm('-e', reported_length))

    # if user specified a length, use it
    length = int(getparm('-l', 0))
    if length > 0:
        end = start + length

if __name__ == '__main__':

    start = 0
    end = 0
    length = 0
    reported_length = 0

    # get the command line parameters
    #filename = "e:\\unzipped\\Pt1_S1_L001_R1_001.fastq"
    #reported_length = os.path.getsize(filename)
    #start = 0
    #end = 10000
    command_line_parameters()
    filename = sys.argv[1]

    # check for invalid start and end values
    if (start < 0) or (start > reported_length) or (end < 0) or (end > reported_length) or (start > end):
        print("Invalid <start>, <end>, or <length> value")
        sys.exit(1)

    
    ####################################
    # open the file
    file = open(filename, 'r')

    # read the portion of the file, echo it to the standard output
    print(readportion(file, start, end))

    # close the file
    file.close()
    ####################################
