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

def main():

    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = GOOGLE_DNS
    transmitter.count = 1
    
    # Counter variable used for writing
    # headers to the CSV file
    file_exists = exists(f'{CSV_FILENAME}.csv')
    if file_exists:
        count = 1
    else:
        count = 0
    
    while(1):
        current_datetime = datetime.datetime.now()
        result = transmitter.ping()
        result_dict = ping_parser.parse(result).as_dict()
        result_subset = {
            "date time": current_datetime.strftime('%x %X'),
            "destination": result_dict["destination"],
            "packet_receive": result_dict["packet_receive"],
            "packet_loss_count": result_dict["packet_loss_count"],
            "rtt_avg": result_dict["rtt_avg"],
        }

        # now we will open a file for writing
        data_file = open(f'{CSV_FILENAME}.csv', 'a', newline='')
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
        
        time.sleep(INTERVAL_S)
    
    
if __name__ == '__main__':
    main()