import requests
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient


def send_it():
    """
    Scrapes metrics from the Arris SURFboard SB6190 status page and sends it to InfluxDB
    """

    url = "http://192.168.100.1/cgi-bin/status"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Startup Procedure
    startup_procedure = soup.find_all('table')[1].find_all('tr')[2:]
    for row in startup_procedure:
        column = row.find_all('td')
        stats = {}
        stats['Procedure'] = column[0].string.strip()
        stats['Status'] = column[1].string.strip()
        stats['Comment'] = column[2].string.strip()
        print(stats)

        client = InfluxDBClient(host='192.168.1.100', port=8086, database='kempferts')
        client.write_points(
            [
                {
                    "measurement": "Arris SURFboard SB6190",
                    "tags": {
                        "status": "Startup Procedure",
                        "procedure": stats['Procedure']

                    },
                    "fields": stats
                }
            ]
        )

    # Downstream Channels
    downstream_channels = soup.find_all('table')[2].find_all('tr')[2:]
    for row in downstream_channels:
        column = row.find_all('td')
        stats = {}
        stats['Channel'] = int(column[0].string.strip())
        stats['Lock Status'] = column[1].string.strip()
        stats['Modulation'] = int(column[2].string.strip('QAM'))
        stats['Channel ID'] = int(column[3].string.strip())
        stats['Frequency'] = float(column[4].string.strip(' MHz'))
        stats['Power'] = float(column[5].string.strip(' dBmV'))
        stats['SNR'] = float(column[6].string.strip(' dB'))
        stats['Corrected'] = int(column[7].string.strip())
        stats['Uncorrectables'] = int(column[8].string.strip())
        print(stats)

        client = InfluxDBClient(host='192.168.1.100', port=8086, database='kempferts')
        client.write_points(
            [
                {
                    "measurement": "Arris SURFboard SB6190",
                    "tags": {
                        "status": "Downstream Bonded Channels",
                        "channel": stats['Channel']
                    },
                    "fields": stats
                }
            ]
        )

    # Upstream Channels
    upstream_channels = soup.find_all('table')[3].find_all('tr')[2:]
    for row in upstream_channels:
        column = row.find_all('td')
        stats = {}
        stats['Channel'] = int(column[0].string.strip())
        stats['Lock Status'] = column[1].string.strip()
        stats['US Channel Type'] = column[2].string.strip()
        stats['Channel ID'] = int(column[3].string.strip())
        stats['Symbol Rate'] = int(column[4].string.strip(' kSym/s'))
        stats['Frequency'] = float(column[5].string.strip(' MHz'))
        stats['Power'] = float(column[6].string.strip(' dBmV'))

        print(stats)

        client = InfluxDBClient(host='192.168.1.100', port=8086, database='kempferts')
        client.write_points(
            [
                {
                    "measurement": "Arris SURFboard SB6190",
                    "tags": {
                        "status": "Upstream Bonded Channels",
                        "channel": stats['Channel']
                    },
                    "fields": stats
                }
            ]
        )


if __name__ == "__main__":
    send_it()
