from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

listings = []

def get_listings_from_search_results(html_file):
    """
    Write a function that creates a BeautifulSoup object on html_file. Parse through the object and return a list of tuples containing: 
    (20 tot. 3 pieces of info each)
        - a string of the title of the listing,
        - an int of the cost to rent for one night, and a string of the listing id number
        - in the format given below. Make sure to turn costs into ints.

    The listing id is found in the url of a listing. For example, for
        https://www.airbnb.com/rooms/1944564
    the listing id is 1944564.
.
    [('Title of Listing 1', 'Cost 1', 'Listing ID 1'),  # format
    ('Loft in Mission District', 210, '1944564'),  # example]

    [('Loft in Mission District', 210, '1944564'), ('Private room in Mission District', 125, '1623609'), ...]
    """
    html = open(html_file, "r").read()
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())

    titles = []
    idlst = []
    prices = []
    output = []

    pricelst = soup.find_all('span', {'class': '_tyxjp1'})
    for p in pricelst:
        prices.append(p.text[1:])
    # print(len(prices))

    listing = soup.find_all('div', {"class": "t1jojoys dir dir-ltr"})
    for tag in listing:
        titles.append(tag.text)
        # print(tag.text)
        rematch = re.findall('\d*', tag.get("id"))
        for str in rematch:
            if len(str)>0:
                idlst.append(str)
    # print(len(idlst))

    for x in range(20):
        toop = (titles[x], prices[x], idlst[x])
        output.append(toop)

    # print(output[-1][0])
    # print(type(output))
    return(output)

    # [('Loft in Mission District', '210', '1944564'), ('Private room in Mission District', '125', '1623609'), ('Private room in Mission District', '137', '11225011'), ('Private room in Mission District', '123', '6600081'), ('Private room in Mission District', '133', '16204265'), ('Guest suite in Mission District', '250', '51106622'), ('Apartment in Mission District', '399', '28668414'), ('Private room in Mission District', '129', '31057117'), ('Private room in Mission District', '129', '38884411'), ('Guest suite in Mission District', '200', '1550913'), ('Private room in Mission District', '82', '51027324'), ('Home in Mission District', '174', '49043049'), ('Guest suite in San Francisco', '174', '23354077'), ('Hotel room in Mission District', '109', '41545776'), ('Guest suite in Mission District', '102', '724897778179485553'), ('Guest suite in Mission District', '285', '10280573'), ('Guest suite in Mission District', '305', '50010586'), ('Apartment in Mission District', '290', '4616596'), ('Private room in Mission District', '114', '23672181'), ('Guest suite in Mission District', '238', '32871760')]

def get_listing_information(listing_id):
    """
    Write a function to return relevant information in a tuple from an Airbnb listing id.
    NOTE: Use the static files in the html_files folder, do NOT send requests to the actual website.
    Information we're interested in:
        string - Policy number: either a string of the policy number, "Pending", or "Exempt"
            This field can be found in the section about the host.
            Note that this is a text field the lister enters, this could be a policy number, or the word "pending" or "exempt" or many others. Look at the raw data, decide how to categorize them into the three categories.
        string - Place type: either "Entire Room", "Private Room", or "Shared Room"
            Note that this data field is not explicitly given from this page. Use the following to categorize the data into these three fields.
                "Private Room": the listing subtitle has the word "private" in it
                "Shared Room": the listing subtitle has the word "shared" in it
                "Entire Room": the listing subtitle has neither the word "private" nor "shared" in it
        int - Number of bedrooms
.
    (policy number, place type, number of bedrooms)
    """
 # ["1623609","1944564","1550913","4616596","6600081"]
# shared: 1944564, 
# entire:
# private: 1623609, 6600081
    html = 'html_files/mission_district_search_results.html'
    htmlfile = open(html, "r").read()
    soup = BeautifulSoup(htmlfile, "html.parser")
    # print(soup.find('div', {"class":"c1l1h97y dir dir-ltr"}))

    # print(listing_id)
    id_title = 'title_' + listing_id

    all_tags = soup.find_all(True)
    for x in range(len(all_tags)):
        # print(all_tags[x])
        if id_title in all_tags[x]:
        # all_tags[x] == id_title in soup.find('span', {"class": "t6mzqp7 dir dir-ltr"}).text:
            print(all_tags[x])
        else:
            continue
        # pass
        # print(tag)
            # print(soup.find('span', {"class": "t6mzqp7 dir dir-ltr"}))
    listing = soup.find_all('div', {"id": id_title})
    # print(listing)
    # content = soup.find('span', {"class": "t6mzqp7 dir dir-ltr"})
    # print(listing)
    # print(content.text)


def get_detailed_listing_database(html_file):
    """
    Write a function that calls the above two functions in order to return the complete listing information using the functions you’ve created.
    This function takes in a variable representing the location of the search results html file.
    The return value should be in this format:

    [
        (Listing Title 1,Cost 1,Listing ID 1,Policy Number 1,Place Type 1,Number of Bedrooms 1),
        (Listing Title 2,Cost 2,Listing ID 2,Policy Number 2,Place Type 2,Number of Bedrooms 2),
        ...
    ]
    """
    html = 'html_files/mission_district_search_results.html'

    first_func = get_listings_from_search_results(html)

    listing_id = []
    for toop in first_func:
        listing_id.append(toop[2])

    sec_func = get_listing_information(listing_id)
    get_listings_from_search_results()
    get_listing_information()

    htmlfile = open(html, "r").read()
    soup = BeautifulSoup(htmlfile, "html.parser")

    output = []
    for toop in first_func:
        for i in sec_func:
            output.append((toop[0], toop[1], toop[2], i[0], i[1], 1[2]))
    return output



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the one that is returned by get_detailed_listing_database()), sorts the tuples in ascending order by cost, writes the data to a csv file, and saves it to the passed filename. The first row of the csv should contain "Listing Title", "Cost", "Listing ID", "Policy Number", "Place Type", "Number of Bedrooms", respectively as column headers. For each tuple in data, write a new row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Listing Title,Cost,Listing ID,Policy Number,Place Type,Number of Bedrooms
    title1,cost1,id1,policy_number1,place_type1,num_bedrooms1
    title2,cost2,id2,policy_number2,place_type2,num_bedrooms2
    title3,cost3,id3,policy_number3,place_type3,num_bedrooms3
    ...

    In order of least cost to most cost.

    This function should not return anything.
    """
    cost_sorted = sorted(data, key=lambda x:x[1])
    headings = ["Listing Title", "Cost", "Listing ID","Policy Number", "Place Type", "Number of Beds"]

    with open("filename","w") as file:
        writer = csv.writer(file)
        writer.writerow([headings])
        for tup in cost_sorted:
            writer.writerow(tup)
        print(tup)
        return None


def check_policy_numbers(data):
    """
    Write a function that takes in a list of tuples called data, (ie. the one that is returned by get_detailed_listing_database()), and parses through the policy number of each, validating the policy number matches the policy number format. Ignore any pending or exempt listings.
    Return the listing numbers with respective policy numbers that do not match the correct format.
        Policy numbers are a reference to the business license San Francisco requires to operate a short-term rental. These come in two forms, where # is a number from [0-9]:
            20##-00####STR
            STR-000####
    .
    Return value should look like this:
    [
        listing id 1,
        listing id 2,
        ...
    ]

    """
    toops_lst = get_detailed_listing_database()
    for toop in toops_lst:
        pass




def extra_credit(listing_id):
    """
    There are few exceptions to the requirement of listers obtaining licenses
    before listing their property for short term leases. One specific exception
    is if the lister rents the room for less than 90 days of a year.

    Write a function that takes in a listing id, scrapes the 'reviews' page
    of the listing id for the months and years of each review (you can find two examples
    in the html_files folder), and counts the number of reviews the apartment had each year.
    If for any year, the number of reviews is greater than 90 (assuming very generously that
    every reviewer only stayed for one day), return False, indicating the lister has
    gone over their 90 day limit, else return True, indicating the lister has
    never gone over their limit.
    """
    pass

def main():
    html = "html_files/mission_district_search_results.html"
    listings = get_listings_from_search_results(html)

    html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"] 
    listing_informations = [get_listing_information(id) for id in html_list]




class TestCases(unittest.TestCase):

    def test_get_listings_from_search_results(self):
        # call get_listings_from_search_results("html_files/mission_district_search_results.html")
        # and save to a local variable
        listings = get_listings_from_search_results("html_files/mission_district_search_results.html")
        # check that the number of listings extracted is correct (20 listings)
        self.assertEqual(len(listings), 20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(listings), list)
        # check that each item in the list is a tuple
        toop_list = get_listings_from_search_results(self)
        for i in toop_list:
            self.assertEqual(type(i), tuple)
        # check that the first title, cost, and listing id tuple is correct (open the search results html and find it)
        self.assertEqual(self.listings[0][0], 'Loft in Mission District')
        self.assertEqual(listings[1][1], '210')
        self.assertEqual(listings[1][2], '1944564')
        # check that the last title is correct (open the search results html and find it)
        self.assertEqual(self.listings[-1][0], 'Guest suite in Mission District')
        

    def test_get_listing_information(self):
        html_list = ["1623609",
                     "1944564",
                     "1550913",
                     "4616596",
                     "6600081"]
        # call get_listing_information for i in html_list:
        listing_informations = [get_listing_information(id) for id in html_list]
        # check that the number of listing information is correct (5)
        self.assertEqual(len(listing_informations), 5)
        for listing_information in listing_informations:
            # check that each item in the list is a tuple
            self.assertEqual(type(listing_information), tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(listing_information), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(listing_information[0]), str)
            self.assertEqual(type(listing_information[1]), str)
            # check that the third element in the tuple is an int
            self.assertEqual(type(listing_information[2]), int)
        # check that the first listing in the html_list has policy number 'STR-0001541'

#         # check that the last listing in the html_list is a "Private Room"

#         # check that the third listing has one bedroom

        pass

    def test_get_detailed_listing_database(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save it to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # check that we have the right number of listings (20)
        self.assertEqual(len(detailed_database), 20)
        for item in detailed_database:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 6

        # check that the first tuple is made up of the following:
        # 'Loft in Mission District', 210, '1944564', '2022-004088STR', 'Entire Room', 1

        # check that the last tuple is made up of the following:
        # 'Guest suite in Mission District', 238, '32871760', 'STR-0004707', 'Entire Room', 1
        pass

    def test_write_csv(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call write csv on the variable you saved
        write_csv(detailed_database, "test.csv")
        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct

        # check that the next row is Private room in Mission District,82,51027324,Pending,Private Room,1

        # check that the last row is Apartment in Mission District,399,28668414,Pending,Entire Room,2
        pass

    def test_check_policy_numbers(self):
        # call get_detailed_listing_database on "html_files/mission_district_search_results.html"
        # and save the result to a variable
        detailed_database = get_detailed_listing_database("html_files/mission_district_search_results.html")
        # call check_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = check_policy_numbers(detailed_database)
        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)
        # check that there is exactly one element in the string

        # check that the element in the list is a string

        # check that the first element in the list is '16204265'
        pass

main()

if __name__ == '__main__':
    database = get_detailed_listing_database("html_files/mission_district_search_results.html")
    write_csv(database, "airbnb_dataset.csv")
    check_policy_numbers(database)
    unittest.main(verbosity=2)
