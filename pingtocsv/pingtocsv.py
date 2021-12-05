import argparse
import csv
import datetime
import json
import time
from os.path import exists

import pingparsing


GOOGLE_DNS = "8.8.8.8"
INTERVAL_S = 5
CSV_FILENAME = "ping log"
TO_KEEP = {
    "destination",
    "packet_receive",
    "packet_loss_count",
    "rtt_avg",
}

def main(args={}):

    csv_filename = args.get('n', CSV_FILENAME)

    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = args.get('ip', GOOGLE_DNS)
    transmitter.count = 1
    
    # Counter variable used for writing
    # headers to the CSV file
    file_exists = exists(f'{csv_filename}.csv')
    if file_exists:
        count = 1
    else:
        count = 0
    
    while(1):
        current_datetime = datetime.datetime.now()
        result = transmitter.ping()
        result_dict = ping_parser.parse(result).as_dict()
        if result_dict["rtt_avg"] is None:
            result_dict["rtt_avg"] = -100
        result_subset = {
            "date time": current_datetime.strftime('%x %X'),
            "rtt": result_dict["rtt_avg"],
            "destination": result_dict["destination"],
            "packet_receive": result_dict["packet_receive"],
            "packet_loss_count": result_dict["packet_loss_count"],
        }

        # now we will open a file for writing
        data_file = open(f'{csv_filename}.csv', 'a', newline='')
        # create the csv writer object
        csv_writer = csv.writer(data_file)

        if count == 0:
            # Writing headers of CSV file
            header = result_subset.keys()
            csv_writer.writerow(header)
            count += 1
    
        # Writing data of CSV file
        csv_writer.writerow(result_subset.values())
        data_file.close()

        print(json.dumps(result_subset, indent=4))
        
        time.sleep(args.get('wait', INTERVAL_S))
    
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ping and log to a csv')
    parser.add_argument('--ip', type=str, default=argparse.SUPPRESS,
                        help='IP address to ping')
    parser.add_argument('--wait', type=int, default=argparse.SUPPRESS,
                        help='after ping returns, seconds to wait before next ping')
    parser.add_argument('-n', type=str, default=argparse.SUPPRESS,
                    help='name of csv file excluding .csv')
    args = vars(parser.parse_args())

    main(args)