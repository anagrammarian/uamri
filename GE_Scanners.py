#!/usr/bin/python

import os
import sys
import glob
import time

fileName = sys.argv[1]
original_working_directory = os.getcwd()
os.chdir(fileName)

def protocol_mapper():
    owd = os.getcwd()
    directoryList = next(os.walk('.'))[1]

    create_matrices(len(directoryList), directoryList)

    return

def parse_all_directories():


    return

def find_key_words(parameter):
    owd = os.getcwd()
    directoryList = next(os.walk('.'))[1]
    key_word_values = ['-' for x in range(len(directoryList)+1)]
    print(key_word_values)
    i = 0
    while (i < len(directoryList)):
       # print(directoryList[i])
        os.chdir(directoryList[i])
        #print(os.getcwd())
        contents = [line.rstrip('\n') for line in open(os.getcwd()+'/LxProtocol')]
        j = 0
        while j < len(contents):
            #print(contents[j])
        # print(i)
            if contents[j].find(' '+parameter+' ') >= 0:
                found = contents[j].split(parameter+' ')[1]
                #print("FOUND!!! \n")
                #print(found)
                key_word_values[i] = found
                j += 1

            else:
                #print('NOT FOUND!!!')
                #key_word_values[j] = '-'
                j += 1

        os.chdir(owd)
        i += 1



    return key_word_values

def create_matrices(num_directories, directoryList):

    if os.path.isfile('GEkeywords') == True:
        ge_parameter_list = [line.rstrip('\n') for line in open('GEkeywords')]  # creates a list by reading parameters from text file
    elif os.path.isfile(os.environ['WIKIPROTPATH']+'/GEkeywords') == True:
        ge_parameter_list = [line.rstrip('\n') for line in open(os.environ['WIKIPROTPATH']+'/GEkeywords')]  # creates a list by reading parameters from text file
    else:
        print('No parameter list found')
        ge_parameter_list = '-'
    parameter_matrix = [['-' for x in range(len(ge_parameter_list) + 1)] for y in range(num_directories+1)]

   #print(len(ge_parameter_list))
    parameter_matrix[0][0] = 'Series'

    i = 0
    while i < len(ge_parameter_list):  #populates custom_parameter_matrix with all the parameters in the first row
        parameter_matrix[0][i+1] = ge_parameter_list[i]
        i += 1

    j = 0
    while j < num_directories:  #populates custom_paameter_matrix with all the parameters in the first row
        parameter_matrix[j+1][0] = directoryList[j].split('_')[0]
        j += 1

    parameter_counter = 0
    for parameter in ge_parameter_list:
        print(parameter)
        key_word_values = find_key_words(parameter)
        print('Values are: ')
        print(key_word_values)

        k=1
        while k <= num_directories:
            #print(key_word_values[k])
            parameter_matrix[k][parameter_counter+1] = key_word_values[k-1]
            k+=1

        parameter_counter += 1

    print(parameter_matrix)
    write_matrices_to_html_file(parameter_matrix, num_directories, len(ge_parameter_list))

    return

def write_matrices_to_html_file(ge_parameter_matrix, num_directories, num_parameters):
    os.chdir(original_working_directory)
    print("Now creating: ")
    f = open(fileName.split('/')[0]+'.htm', 'w+')
    #print('CREATING NEW HTML')
    f.write('<!DOCTYPE html> \n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<style>\n')
    f.write('table, th, td {\n')
    f.write('\t border: 1px solid black;\n')
    f.write('}\n')
    f.write('th, td { \n \t padding: 15px;\n}')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')

    i = 1
    #print('Protocol num is: ' + str(protocol_num))


    f.write('<h2>')
    f.write('Table for '+fileName.split('-')[0])
    f.write('</h2>\n')

    f.write('<table style="width:100%">\n')

    writeCounterColumn1 = 0

    while writeCounterColumn1 < 1:

        writeCounterRow1 = 0

        f.write('<table style="background-color:#FFFFE0;"> \n')
        f.write('<tr style="background-color:#BDB76B;color:ffffff;"> \n')
        while writeCounterRow1 <= num_parameters:
            f.write('<th>')
            f.write(str(ge_parameter_matrix[writeCounterColumn1][writeCounterRow1]))
            f.write('</th>')
            writeCounterRow1 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn1 += 1

    writeCounterColumn1 = 1

    while writeCounterColumn1 < num_directories + 1:

        writeCounterRow1 = 0
        f.write('<tr>')
        while writeCounterRow1 <= num_parameters:
            f.write('<td>')
            f.write(ge_parameter_matrix[writeCounterColumn1][writeCounterRow1])
            f.write('</td>')
            writeCounterRow1 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn1 += 1

    f.write('</table>\n')
    f.write('<br>')
    f.write('</br>')
    f.write('\n')
    f.write('<br>')
    f.write('</br>')
    f.write('<textarea rows="6" cols="140">')
    f.write('Insert notes here')
    f.write('</textarea>')
    f.write('<br>')
    f.write('</br>')
    f.write('<textarea rows="6" cols="140">')
    f.write('Indications')
    f.write('</textarea>')
    f.write('<br>')
    f.write('</br>')

    f.write('\n')
    f.write('<br>')
    f.write('</br>')
    f.write('</body>\n')
    f.write('</html>\n')
    f.close()

    return


protocol_mapper()