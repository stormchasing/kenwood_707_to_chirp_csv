import re
import os

from glob import glob

pattern = re.compile(r'[0-9]{3}\t([0-9]{11})\t\d\t(\d)\t\d\t(\d)\t\d\t\t(\d\d)\t\t\d\d\t\t\d\t\t\t\t\t([0-9A-Z\. ]+)')
tone_map = ['0', '67.0', '69.3', '71.9', '74.4', '77.0', '79.7', '82.5', '85.4', '88.5', '91.5', '94.8', '97.4',
            '100.0', '103.5', '107.2', '110.9', '114.8', '118.8', '123.0', '127.3', '131.8', '136.5', '141.3', '146.2',
            '151.4', '156.7', '162.2', '167.9', '173.8', '179.9', '186.2', '192.8', '203.5', '206.5', '210.7', '218.1',
            '225.7', '229.1', '233.6', '241.8', '250.3', '254.1']

files = glob('/Users/jhehnly/Google Drive/files/Kenwood Radio Programming/Mcp-G707/*.707')
for filename in files:
    print filename
    target = open('/Users/jhehnly/Google Drive/files/chirp/' + os.path.basename(filename).replace('707', 'csv'), 'w')
    target.write('Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,' +
                 'Skip,Comment,URCALL,RPT1CALL,RPT2CALL\n')
    with open(filename) as f:
        lines = f.readlines()
        row_index = 1
        for line in lines:
            match = pattern.match(line)
            if match is not None:
                raw_frequency, offset_raw, raw_use_tone, raw_tone, raw_name = match.groups()
                frequency = str(float(raw_frequency)/1000000).ljust(10, '0')
                if offset_raw == '1':
                    offset_shift = '+'
                elif offset_raw == '2':
                    offset_shift = '-'
                else:
                    offset_shift = ''
                offset = '0.600000' if float(raw_frequency)/1000000 < 200 else '5.000000'
                if raw_use_tone == '1':
                    tone_mode = 'Tone'
                    tone = tone_map[int(raw_tone)]
                else:
                    tone_mode = ''
                    tone = '88.5'
                name = raw_name.strip()
                if name == 'SIMPLEX':
                    name = 'SIM' + frequency[2:6]
                name = name.replace('.', '')[:6]

                target.write('%s,%s,%s,%s,%s,%s,%s,88.5,023,NN,FM,5.00,,,,,,\n' % (
                    row_index,
                    name,
                    frequency,
                    offset_shift,
                    offset,
                    tone_mode,
                    tone))
                row_index += 1
    target.close()
