import csv
''' Module for writing data into a csv file.'''

def true_to_yes(b):
    if b:
        return 'Yes'
    else:
        return ''

def dict_to_csv(savefile, rest_dict):
    ''' Write the list of businesses into the csv file specified. '''

    with open(savefile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header.
        writer.writerow([
                        'Business Name',
                        'Keywords',
                        'Area',
                        'Address',
                        'Phone',
                        'Website',
                        'Message Form',
                        'Reservation Form',
                        'Takes Reservation'
                        ])

        for name, info in rest_dict.items():
            writer.writerow([
                            name,
                            ' '.join(info['genre']),
                            info['area'],
                            info['address'],
                            info['phone'],
                            info['web'],
                            true_to_yes(info['message']),
                            true_to_yes(info['reservation']),
                            info['takes_rsrv']
                            ])
