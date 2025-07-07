"""
File: webcrawler.py
Name: Meg
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10905209
Female Number: 7949058
---------------------------
2000s
Male Number: 12979118
Female Number: 9210073
---------------------------
1990s
Male Number: 14146775
Female Number: 10644698
"""

import requests
from bs4 import BeautifulSoup


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # ----- Write your code below this line ----- #

        tags = soup.find_all('tbody')
        for tag in tags:
            text = tag.text
            wanted_text = text[:len(text)-140]                # Remove the unwanted words.
            tokens = wanted_text.split()
            male_number = 0
            female_number = 0
            for i in range(len(tokens)):
                if i % 5 == 2:
                    male_num_token = tokens[i].split(',')     # Change number(str) to number(int)
                    male_num = int(male_num_token[0])*1000+int(male_num_token[1])
                    male_number += male_num
                if i % 5 == 4:
                    female_num_token = tokens[i].split(',')   # Change number(str) to number(int)
                    female_num = int(female_num_token[0]) * 1000 + int(female_num_token[1])
                    female_number += female_num
            print(f"Male Number: {male_number}")
            print(f"Female Number: {female_number}")


if __name__ == '__main__':
    main()
