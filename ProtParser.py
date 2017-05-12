#!/usr/bin/python
#Version 2.3: Has ability to parse multiple programs in one xml to one html page. Converts all xml_files to underscore.
#   Also, works on xml files with multiple step-engine-controls. Matrix works correctly. Speed has been improved.
#Before change in while loops in find_key_word, parsing BRN TUMOR.xml took 2:00 minutes
import os
import sys
import glob
import time

import xml.etree.ElementTree as ET  # imports element tree function


#print('Running from ')
#print(os.cwd())


#tree = ET.parse(xml_file)  # uses ET function on the xml file
#root = tree.getroot()  # creates root function for calling roots from the xml file. root[0] calls the first child in the element tree

def find_key_word(xml_file, key_word, engine_num, overall_series_count, current_series_count):
    tree = ET.parse(xml_file)  # uses ET function on the xml file
    root = tree.getroot()  # creates root function for calling roots from the xml file. root[0] calls the first child in the element tree

    j = overall_series_count - current_series_count
    key_value_counter = 0
    total_scan_time = '0:0'

    #print(overall_series_count)
    #print(current_series_count)
    #print(j)
    #print('\n')

    key_word_value = ['-' for i in range(current_series_count+1)]
    if j == 0:
        j = 1
    else:
        j = j + 1
    #print('These are initial key word values')
    #print(key_word_value)
    while j < overall_series_count + 1:
        k = 1

        if key_word.split('->')[0] == 'Scan time' and (j < overall_series_count + 1):
            try:
                total_scan_time = str(int(total_scan_time.split(':')[0]) + int(root[j][0][1][0][1].text[3:9].split(':')[0])
                                    + (int(total_scan_time.split(':')[1])
                                       + int(root[j][0][1][0][1].text[3:9].split(':')[1]))
                                    // int(60)) + ':' + str((int(total_scan_time.split(':')[1])
                                                             + int(root[j][0][1][0][1].text[3:9].split(':')[1])) % 60)
                time_looper = 0

                while time_looper < len(root[j][0][1][0][1].text.split(' ')):
                    #print(root[j][0][1][0][1].text.split(' ')[time_looper])
                    if 'TA:' in root[j][0][1][0][1].text.split(' ')[time_looper]:
                        #print(root[j][0][1][0][1].text.split(' ')[time_looper + 1])
                        #print('\n')
                        key_word_value[key_value_counter] = root[j][0][1][0][1].text.split(' ')[time_looper + 1]
                        time_looper = len(root[j][0][1][0][1].text.split(' '))

                    time_looper += 1
                #key_word_value[key_value_counter] = root[j][0][1][0][1].text[3:9]

                k = 100
            except Exception:
                k = 100
                pass

        #print(j)
        #print(len(root[j][0][1]))
        #print('\n')

        while k < len(root[j][0][1]): #len(root[j][0][1]):

            l = 0
            #print(j)
            #print(k)
            parameter_count = len(root[j][0][1][k])
            #print(len(root[j][0][1][k]))
            #print('\n')

            while l <= parameter_count: #len(root[j][0][1][k]):

                try:
                    if key_word.split('->')[0] == 'PAT':
                        pat_looper = 0

                        while pat_looper < len(root[j][0][1][0][1].text.split(' ')):
                            if root[j][0][1][0][1].text.split(' ')[pat_looper] == 'mmPAT:':
                                key_word_value[key_value_counter] = root[j][0][1][0][1].text.split(' ')[pat_looper+1]
                                pat_looper = len(root[j][0][1][0][1].text.split(' '))
                            pat_looper += 1


                    if key_word.split('->')[0] == root[j][0][1][k][l][0].text:  # check to see if search item has been found
                        #print('KEY WORD FOUND!')
                        key_word_value[key_value_counter] = root[j][0][1][k][l][1].text  # places the parameter value in the key_wokrd_value array
                        k = 100  # sets k and l to 100 to break out of the two while loops so that we can move to the next
                        l = 100  # protocol, which prevents redundancies



                except Exception:  # prevents error from stopping script when element does not exist
                    pass

                l += 1
            k += 1
        j += 1
        key_value_counter += 1

    return (key_word_value, total_scan_time)

def prot_mapper(xml_for_mapping):
    #print('XML entering prot_mapper')
    #print(xml_for_mapping)
    #print('\n')

    print('This is file name for parsing:')
    print(xml_for_mapping)



    import space_to_underscore
    xml_for_mapping = space_to_underscore.spaceToUnderscore(xml_for_mapping)

    #print('This is file name for parsing:')
    #print(xml_for_mapping)

    tree = ET.parse(xml_for_mapping)  # uses ET function on the xml file
    root = tree.getroot()  # creates root function for calling roots from the xml file. root[0] calls the first child in the element tree

    k = 0
    engine_num = 0
    current_series_num = 0
    overall_series_count = 0
    while k < len(root[0][0][2][0]):
        engine_name = root[0][0][2][0][k].get('name')

        #print(k)
        #print('\n')


        i = 0
        protocol_num = 0

        while i < 100:
            try:
                check = root[0][0][2][0][k][i].get('name')
                i += 1
                protocol_num = i
            except Exception:
                i = 100
                pass
        print("The number of sub protocols found in %s from the %s file is: %d" %(engine_name, xml_for_mapping, protocol_num))
        print('\n')
        i = 0
        j = 0



        file_name = engine_name.replace(" ", "_") + '.htm'
        currentPath = os.getcwd()
        file_name = currentPath + "/" + file_name


        if os.path.exists(file_name):
            os.remove(file_name)

        while i <= protocol_num:  # this while loop finds the number of protocols

            try:
                check = root[0][0][2][0][k][i][j].get('name')
                j += 1


            except Exception:
                current_series_num = j  # - tocExists
                overall_series_count = overall_series_count + j

                if current_series_num != 0:
                    create_parameter_matrices(xml_for_mapping, i, k, engine_name, overall_series_count, current_series_num, protocol_num)  # middle argument may need to be i+1
                i += 1
                j = 0
                current_series_num = 0
                pass
        k += 1
    return

def create_parameter_matrices(xml_file, prot_num, engine_num, engine_name, overall_series_num, current_series_num, protocol_num):

    tree = ET.parse(xml_file)  # uses ET function on the xml file
    root = tree.getroot()  # creates root function for calling roots from the xml file. root[0] calls the first child in the element tree

    if os.path.isfile('customParameters.txt') == True and os.path.isfile('complexParameters.txt') == True:
        custom_parameter_list = [line.rstrip('\n') for line in open('customParameters.txt')]  # creates a list by reading parameters from text file

        complex_parameter_list = [line.rstrip('\n') for line in open('complexParameters.txt')]

    elif os.path.isfile(os.environ['WIKIPROTPATH'] + '/customParameters.txt') == True \
            and os.path.isfile(os.environ['WIKIPROTPATH'] + '/complexParameters.txt') == True:
        custom_parameter_list = [line.rstrip('\n') for line in open(os.environ['WIKIPROTPATH']
                                                                    + '/customParameters.txt')]  # creates a list by reading parameters from text file
        complex_parameter_list = [line.rstrip('\n') for line in open(os.environ['WIKIPROTPATH']
                                                                     + '/complexParameters.txt')]
    else:
        print('customParameters.txt and/or complexParameters.txt not found!')
        sys.exit()

    custom_parameter_matrix = [['-' for x in range(len(custom_parameter_list)+1)] for y in range(current_series_num + 1)]  # creates a 2D array with size parameter list by protocol number
    complex_parameter_matrix = [['-' for x in range(current_series_num + 1)] for y in range(len(complex_parameter_list) + 1)]
    custom_parameter_matrix[0][0] = 'Series'
    complex_parameter_matrix[0][0] = 'Sequence Parameters'

    i = 0
    total_scan_time = 'Scan time not available'

    while i < len(custom_parameter_list):  #populates custom_parameter_matrix with all the parameters in the first row

        custom_parameter_matrix[0][i+1] = custom_parameter_list[i].split('->')[1]

        i += 1

    j = 0

    while j < len(complex_parameter_list): #populates complex_parameter_matrix with all the parameters in the first column
        complex_parameter_matrix[j+1][0] = complex_parameter_list[j].split('->')[1]

        j += 1

    m = 0
    while m < current_series_num:
        custom_parameter_matrix[m+1][0] = root[0][0][2][0][engine_num][prot_num][m].get('name')
        complex_parameter_matrix[0][m + 1] = root[0][0][2][0][engine_num][prot_num][m].get('name')
        m += 1
    #print('Before population')
    #print(custom_parameter_matrix)
    #print('\n')
    #print(complex_parameter_matrix)
    #print('\n')


    custom_parameter_counter = 0
    for parameter in custom_parameter_list: #loop through all parameters in custom_parameter_list to find all the values for each series

        total_scan_time = find_key_word(xml_file, parameter, engine_num, overall_series_num, current_series_num)[1]

        if parameter.split('->')[0] == 'Notes':
            custom_parameter_counter += 1
            pass

        elif parameter.split('->')[0] == 'Matrix':
            base_resolution = ['-' for i in range(current_series_num)]
            phase_resolution = ['-' for i in range(current_series_num)]
            #matrix_matrix = ['-' for i in range(current_series_num)]
            base_resolution = find_key_word(xml_file, 'Base resolution', engine_num, overall_series_num, current_series_num)[0]
            phase_resolution = find_key_word(xml_file, 'Phase resolution', engine_num, overall_series_num, current_series_num)[0]

            i = 1
            while i < current_series_num + 1:
                #print(base_resolution[i-1])
                #print(phase_resolution[i-1])
                #print('\n')

                if base_resolution[i-1] != '-' and phase_resolution[i-1] != '-':
                    custom_parameter_matrix[i][custom_parameter_counter+1] = str(base_resolution[i-1]) + 'X '+ str(int(base_resolution[i-1]) * int(phase_resolution[i-1].split("%")[0]) / 100)
                else:
                    custom_parameter_matrix[i][custom_parameter_counter + 1] = '-'
                i += 1

            custom_parameter_counter += 1

        else:
            #print(find_key_word(xml_file, parameter, overall_series_num, current_series_num)[0])
            key_word_values = ['-' for i in range(current_series_num)]
            key_word_values = find_key_word(xml_file, parameter, engine_num, overall_series_num, current_series_num)[0]


            k = 1
            while k < current_series_num + 1:   #loops through the 1D array of the parameter values for each series

                custom_parameter_matrix[k][custom_parameter_counter+1] = key_word_values[k-1]

                k += 1
            custom_parameter_counter += 1

    complex_parameter_counter = 0
    for parameter in complex_parameter_list:    #loop through all parameters in complex_parameter_list to find all the values for each series


        total_scan_time = find_key_word(xml_file, parameter, engine_num, overall_series_num, current_series_num)[1]
        if parameter.split('->')[0] == 'Notes':
            complex_parameter_counter += 1
            pass
        elif parameter.split('->')[0] == 'Matrix':
            base_resolution = ['-' for i in range(current_series_num)]
            phase_resolution = ['-' for i in range(current_series_num)]
            # matrix_matrix = ['-' for i in range(current_series_num)]
            base_resolution = find_key_word(xml_file, 'Base resolution', engine_num, overall_series_num, current_series_num)[0]
            phase_resolution = find_key_word(xml_file, 'Phase resolution', engine_num, overall_series_num, current_series_num)[0]

            i = 1
            while i < current_series_num + 1:
                #print(base_resolution[i-1])
                #print(phase_resolution[i-1])
                #print('\n')

                if base_resolution[i - 1] != '-' and phase_resolution[i - 1] != '-':
                    complex_parameter_matrix[complex_parameter_counter + 1][i] = str(base_resolution[i - 1]) + 'X ' + str(
                        int(base_resolution[i - 1]) * int(phase_resolution[i - 1].split("%")[0]) / 100)
                else:
                    complex_parameter_matrix[complex_parameter_counter + 1][i] = '-'
                i += 1

            complex_parameter_counter += 1
        else:
            key_word_values = ['-' for i in range(current_series_num)]
            key_word_values = find_key_word(xml_file, parameter, engine_num, overall_series_num, current_series_num)[0]

            k = 1
            while k < current_series_num + 1:   #loops through the 1D array of the parameter values for each series


                complex_parameter_matrix[complex_parameter_counter+1][k] = key_word_values[k-1]


                k += 1
            complex_parameter_counter += 1
    #print('After searching keywords')
    #print(custom_parameter_matrix)
    #print('\n')
    #print(complex_parameter_matrix)
   # print('\n')


    write_matrices_to_html_file(xml_file, custom_parameter_matrix, complex_parameter_matrix, total_scan_time, len(custom_parameter_list), len(complex_parameter_list), engine_num, engine_name, prot_num, current_series_num, protocol_num)

    return

def write_matrices_to_html_file(xml_file, custom_parameter_matrix, complex_parameter_matrix, total_scan_time, custom_parameter_num, complex_parameter_num, engine_num, engine_name, prot_num, series_num, protocol_num):
    tree = ET.parse(xml_file)  # uses ET function on the xml file
    root = tree.getroot()  # creates root function for calling roots from the xml file. root[0] calls the first child in the element tree

    seriesName = root[0][0][2][0][0][prot_num].get('name') #xml_file.split('.xml')[0]#+'-'+root[0][0][2][0][0][prot_num].get('name')
    seriesNameFile = seriesName.replace(" ", "_")
    engine_name = engine_name.replace(" ", "_")
    seriesName = engine_name + '.htm'#seriesName.replace("/", "_") + '-' + engine_name + '.htm'
    currentPath = os.getcwd()
    seriesNameFile = currentPath + "/" + seriesName


    toc_exists = 0

    if root[0].tag == 'PrintTOC':
        toc_exists = 1
    else:
        toc_exists = 0

    if os.path.exists(seriesNameFile):
        f = open(seriesNameFile, 'r')
        #print('WILL ADD TO CURRENT HTML')
        f.seek(0)
        s = f.read()
        R = s.split('</body>')
        f.close()

        f = open(seriesNameFile, 'w+')
        f.write(R[0])
    else:
        print("Now creating: " + seriesName)
        f = open(seriesNameFile, 'w+')
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
    if toc_exists == 1:

        while i <= protocol_num:
            #print(i)
            f.write('<a href="#' + str(i)+'"')
            f.write('>')
            f.write('Jump to Table ' + str(i))
            f.write('</a>')
            f.write('\n')
            i+=1

        f.write('<h2 id="'+str(prot_num+1)+'">')
        f.write(root[0][0][2][0][engine_num][prot_num].get('name')) #root[0][0][2][0][0][0].get('name')+'-'+root[0][0][2][0][0][prot_num].get('name'))

        f.write(' (Total scan time: ' + total_scan_time.split(':')[0] + ':' + total_scan_time.split(':')[1] + ')')
        f.write('</h2>\n')
        f.write('<h2>')
        f.write('Overview')
        f.write('</h2>\n')

    else:
        while i <= protocol_num:
            #print(i)
            f.write('<a href="#' + str(i) + '"')
            f.write('>')
            f.write('Jump to Table ' + str(i))
            f.write('</a>')
            f.write('\n')
            i += 1

        f.write('<h2 id="' + str(prot_num+1) + '">')
        f.write(root[0][0][2][0][engine_num][prot_num].get('name'))
        #f.write(root[0][0][1][0][0].text[35:49]+'-'+root[0][0][2][0][0][prot_num].get('name'))

        f.write(' (Total scan time: ' + total_scan_time.split(':')[0] + ':' + total_scan_time.split(':')[1] + ' min)')
        f.write('</h2>\n')

    f.write('<table style="width:100%">\n')

    writeCounterColumn1 = 0

    while writeCounterColumn1 < 1:

        writeCounterRow1 = 0

        f.write('<table style="background-color:#FFFFE0;"> \n')
        f.write('<tr style="background-color:#BDB76B;color:ffffff;"> \n')
        while writeCounterRow1 < custom_parameter_num:
            f.write('<th>')
            f.write(str(custom_parameter_matrix[writeCounterColumn1][writeCounterRow1]))
            f.write('</th>')
            writeCounterRow1 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn1 += 1

    writeCounterColumn1 = 1

    while writeCounterColumn1 < series_num + 1:

        writeCounterRow1 = 0
        f.write('<tr>')
        while writeCounterRow1 < custom_parameter_num:
            f.write('<td>')
            f.write(custom_parameter_matrix[writeCounterColumn1][writeCounterRow1])
            f.write('</td>')
            writeCounterRow1 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn1 += 1

    f.write('</table>\n')
    f.write('<br>')
    f.write('</br>')
    f.write('\n')
    f.write('<table style="width:100%">\n')

    writeCounterColumn2 = 0
    f.write('<h2>\n')
    f.write('Detailed')
    f.write('\n')
    f.write('</h2>\n')
    while writeCounterColumn2 < 1:

        writeCounterRow2 = 0

        f.write('<table style="background-color:#CAE8FC;"> \n')
        f.write('<tr style="background-color:#0613D7;color:#FBFBFC;"> \n')
        while writeCounterRow2 < series_num + 1:
            f.write('<th>')
            f.write(complex_parameter_matrix[writeCounterColumn2][writeCounterRow2])
            f.write('</th>')
            writeCounterRow2 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn2 += 1



    writeCounterColumn2 = 1

    while writeCounterColumn2 < complex_parameter_num: # maybe help?- 1:

        writeCounterRow2 = 0
        f.write('<tr>')
        #while writeCounterRow2 < series_num + 1:#add one?
        while writeCounterRow2 < len(complex_parameter_matrix[writeCounterColumn2]):
            f.write('<td>')
            f.write(complex_parameter_matrix[writeCounterColumn2][writeCounterRow2])
            f.write('</td>')
            writeCounterRow2 += 1
        f.write('</tr>')
        f.write('\n')
        writeCounterColumn2 += 1

    f.write('</table>\n')
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
    f.write('<img src=')
    f.write('"')
    f.write(xml_file.split('xml')[0])
    f.write('jpg')
    f.write('"')
    f.write(' alt="Placer Image" style="width:304px;height:228px;">')
    f.write('\n')
    f.write('\n')
    f.write('<br>')
    f.write('</br>')
    f.write('</body>\n')
    f.write('</html>\n')
    f.close()
    return

def parse_all_prots():

    currentPath = os.getcwd()
    path = currentPath + "/*.xml"

    for gname in glob.glob(path):
        tree = ET.parse(gname.split('/')[len(gname.split('/'))-1])
        root = tree.getroot()

        g = os.path.getmtime(gname)
        gname = gname.split('/')[len(gname.split('/'))-1]
        seriesName = gname.split('.xml')[0] + '-' + root[0][0][2][0][0][0].get('name')
        htmlFile = seriesName.replace(" ", "_")
        htmlFile = seriesName.replace("/", "_") + '.htm'
        if os.path.exists(htmlFile):
            f = os.path.getmtime(htmlFile)

            if f < g:
                #print(gname)
                prot_mapper(gname)

            else:
                print('ProtParser has already run on ' + gname + '\n')

        else:
            #print(gname)
            prot_mapper(gname)
    return

def move_through_directories_recursively():
    print('Will now run ProtParser on all xml files in directories in form like this: '
          '"$WIKIPROTPATH/Scanners/SCANNER_NAME/NEURO"')
    owd = os.environ['WIKIPROTPATH'] + '/Scanners/'
    os.chdir(owd)

    directoryList1 = next(os.walk('.'))[1]

    i = 0
    while (i < len(directoryList1)):
        if (directoryList1[i] != 'apps'):
            if (directoryList1[i] != 'files'):
                if (directoryList1[i] != 'uploads'):
                    if (directoryList1[i] != '.idea'):

                        os.chdir(directoryList1[i])
                        # print(directoryList1[i])
                        directoryList2 = next(os.walk('.'))[1]
                        sowd = os.getcwd()

                        j = 0
                        while (j < len(directoryList2)):
                            if (directoryList2[j] != 'apps'):
                                if (directoryList2[j] != 'files'):
                                    if (directoryList2[j] != 'uploads'):
                                        if (directoryList2[j] != '.idea'):

                                            branch_directory = directoryList2[j]
                                            os.chdir(branch_directory)
                                            parse_all_prots()
                                            os.chdir(sowd)
                            j = j + 1
                        os.chdir(owd)
        i = i + 1

    return

def parsing_options():
    if len(sys.argv) != 2:
        print('"ProtParser.py <xml_file_name> or <all_in_cwd> or <all_directories>"')
        sys.exit()

    else:
        xml_file = sys.argv[1]

    if xml_file.endswith('all_in_cwd') or xml_file.endswith('ALL_IN_CWD'):
        print('All xml files in current directory will be run through protParser now!')
        parse_all_prots()

    elif xml_file.endswith('all_directories') or xml_file.endswith('ALL_DIRECTORIES'):
        move_through_directories_recursively()
    else:
        if xml_file.endswith('.xml'):
            if os.path.exists(xml_file):
                prot_mapper(xml_file)
            else:
                print("File not found!")
        else:
            print('File name must end in .xml. ')
            print('"ProtParser.py <xml_file_name> or <all_in_cwd> or <all_directories>"')

    return

parsing_options()