import argparse
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate







banner = R"""
<============================================================================>
| +------------------------------------------------------------------------+ |
|+|                                                                        |+|
|+|  ____       _     ____  _           _                _                 |+|
|+| |  _ \ __ _| | __/ ___|(_)_ __ ___ | |    ___   ___ | | ___   _ _ __   |+|
|+| | |_) / _` | |/ /\___ \| | '_ ` _ \| |   / _ \ / _ \| |/ / | | | '_ \  |+|
|+| |  __/ (_| |   <  ___) | | | | | | | |__| (_) | (_) |   <| |_| | |_) | |+|
|+| |_|   \__,_|_|\_\|____/|_|_| |_| |_|_____\___/ \___/|_|\_\\__,_| .__/  |+|
|+|                                                                |_|     |+|
|+|                                                                   v1.1 |+|
|+|                                                                        |+|
|+|                "Uncover Connections. Reveal Identities."               |+|
| +------------------------------------------------------------------------+ |
<============================================================================>
| >GitHub    : https://github.com/0kraven                                    |
| >LinkedIn  : https://www.linkedin.com/in/0xkabeer                          |
| >Instagram : https://www.instagram.com/@echomekabeer                       |
<============================================================================>
| Crafted by [0kraven] - The Architect of PakSimLookup                       |
| Initialize(); // PakSimLookup.start()                                      |
<============================================================================>
"""

# Function to validate the phone number (should start with 0)
def validate_phone_number(number):
    if number.startswith("0") and len(number) == 11 and number.isdigit():
        return True
    else:
        print("Error: The phone number must start with 0 and be 11 digits long.")
        return False

# Function to validate the CNIC (should be without dashes)
def validate_cnic(cnic):
    if len(cnic) == 13 and cnic.isdigit():
        return True
    else:
        print("Error: CNIC should be 13 digits long and without dashes.")
        return False

# Function to fetch CNIC using the phone number
def fetch_cnic_from_sim_owner(number):
    url = "https://sim-owner-details.info/wp-admin/admin-ajax.php"
    data = {"action": "handle_sim_owner_search", "mobileNumber": number}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('success') and 'results' in json_response:
                return json_response['results'].get('CNIC')

    except requests.exceptions.RequestException:
        print("Connection error with sim-owner-details.info")
        return None

# Function to fetch details from numberdetails.xyz
def fetch_details_from_numberdetails(cnic):
    url = "https://numberdetails.xyz/"
    headers = {
        "Host": "numberdetails.xyz",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://numberdetails.xyz/"
    }
    data = {"searchinfo": cnic}
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', class_='result-card')
            table = []
            

            for card in cards:
                fields = card.find_all('div', class_='field')
                name = card.find('label', string='FULL NAME').find_next('div').text.strip()
                phone = card.find('label', string='PHONE #').find_next('div').text.strip()
                address = card.find('label', string='ADDRESS').find_next('div').text.strip()
                
                table.append([name, phone, cnic, address])

            return table
        else:
            print("Failed to retrieve details from numberdetails.xyz")
            return None
    except requests.exceptions.RequestException:
        print("Connection error with numberdetails.xyz")
        return None

# Function to handle argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Pakistan SIM Lookup Tool',
        add_help=False  # Disable default help
    )
    parser.add_argument('--number', type=str, help='Phone number to look up details')
    parser.add_argument('--cnic', type=str, help='CNIC number to look up details')
    parser.add_argument('--help', action='store_true', help='Show help message')
    return parser.parse_args()

# Main function to drive the script
def main():
    args = parse_arguments()
    details = []
    if args.help:
        help = """
<=========================== PakSimLookup Manual ===============================>
|+|                                                                           |+|
|+| Welcome to PakSimLookup Tool!                                             |+|
|+|                                                                           |+|
|+| Options:                                                                  |+|
|+| --number [NUMBER] : Lookup details by phone number (format: 03XXXXXXXXXX) |+|
|+| --cnic [CNIC]     : Lookup details by CNIC (13 digits, no dashes)         |+|
|+| --help            : Enter help mode for interactive input                 |+|
|+|                                                                           |+|
|+| Manual Mode:                                                              |+|
|+| - Choose to search by either phone number or CNIC.                        |+|
|+| - Enter the required information when prompted.                           |+|
|+|                                                                           |+|
|+| Example Usages:                                                           |+|
|+| python3 paksimlookup.py --number 923001234567                             |+|
|+| python3 paksimlookup.py --cnic 1234567890123                              |+|
|+| python3 paksimlookup.py --help                                            |+|
|+|                                                                           |+|
<===============================================================================>
        """
        print(help)
        return None
    else:
        print(banner)
    if args.number:
        if validate_phone_number(args.number):
            cnic = fetch_cnic_from_sim_owner(args.number)
            if cnic:
                details = fetch_details_from_numberdetails(cnic)
        else:
            return None
    elif args.cnic:
        if validate_cnic(args.cnic):
            details = fetch_details_from_numberdetails(args.cnic)
    else:
        print("Usage: paksimlookup.py [--number NUMBER] [--cnic CNIC] [--help]")
        return None
    if details:
        print(tabulate(details, headers=["Full Name", "Phone", "CNIC", "Address"], tablefmt="grid"))
    else:
        print("No Data Found.")


# Entry point of the script
if __name__ == '__main__':
    main()
