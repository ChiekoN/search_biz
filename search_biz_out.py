import csv
import sys
import search_biz_tk as sbtk
# ----------------------------------------------------------
# Module for writing data into a csv file.
#
# Ver. 1.0 released on 25/05/2018
# Author: Chieko N.
# -----------------------------------------------------------

def true_to_yes(b):
    if b:
        return 'Yes'
    else:
        return ''

def dict_to_csv(savefile, rest_dict, parent_window):
    """ Write the list of businesses into the csv file specified. """

    while True:
        try:
            csvfile = open(savefile, 'w', encoding='utf-8',
                            errors='ignore', newline='')
            break

        except OSError:
            err = str(sys.exc_info()[0])+' : '+str(sys.exc_info()[1])
            print("Output file cannot open. ({})".format(err))
            if not sbtk.retry_errormessage(parent_window,
                                            'File open error.', err):
                raise   # If Cancel pressed, raise Exception and quit.
                        # If Retry pressed, go back to loop and retry file open.

    try:
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
                        'Takes Reservation',
                        'Page on yelp'
                        ])

        for id, info in rest_dict.items():
            writer.writerow([
                            info['name'],
                            ' '.join(info['genre']),
                            info['area'],
                            info['address'],
                            info['phone'],
                            info['web'],
                            true_to_yes(info['message']),
                            true_to_yes(info['reservation']),
                            info['takes_rsrv'],
                            info['page']
                            ])
    except csv.Error:
        err_csv = str(sys.exc_info()[0])+' : '+str(sys.exc_info()[1])
        print("CSV write error. ({})".format(err_csv))
        sbtk.show_errormessage(parent_window,
                            'CSV write error. Program terminated.',
                            err_csv)
    except:
        any_err = str(sys.exc_info()[0])+' : '+str(sys.exc_info()[1])
        print("Error in writing file. ({})".format(err_csv))
        sbtk.show_errormessage(parent_window,
                            'Error in file writing process. Program terminated.',
                            any_err)
    finally:
        csvfile.close()
