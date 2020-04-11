import csv
S3_PATH = "https://airbnb-sample.s3.eu-west-2.amazonaws.com/"
OUTPUT_FILE = "airbnb_urls.csv"

def get_successful_urls(service):
    PROCESSING_DATA_PATH = "../tables/{}_AirBnb.csv".format(service)
    with open(PROCESSING_DATA_PATH, newline='') as processing_data_csv:
        column0 = []
        csvreader = csv.reader(processing_data_csv, delimiter=' ', quotechar='|')
        for row in csvreader:
            column0.append(row[0].split(",")[0])
    if service == "microsoft":
        # Note: the microsot output table already contains the URLs as identifiers
        # (so no need to add the path prefix to form a URL)
        return column0[1:]
    return [S3_PATH + x for x in column0[1:]]

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("URL",))
        for row in data:
            csvwriter.writerow((row,))

apis = ["microsoft", "amazon", "clarifai", "face++"]

sets_of_urls = [set(get_successful_urls(x)) for x in apis]
shared_urls = set.intersection(*sets_of_urls)

write_to_csv(shared_urls)
