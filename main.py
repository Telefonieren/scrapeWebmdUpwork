import requests
from bs4 import BeautifulSoup
import csv

# This script goes through all the pages of doctors list by itself
# Paste the link on the specialists list page below
# Result CSV file will have a name {Speciality} near {City}, {State}

URL = 'https://doctor.webmd.com/providers/specialty/pediatric-gastroenterology/new-york/new-york' # The only link to change



HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

CSV_HEADER = ['Doctor Name','Clinic','Clinic address','Phone','Web link']
req = requests.get(URL, HEADERS)
src = req.text

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)

soup = BeautifulSoup(src, 'lxml')

page_number = soup.find(class_='btn-next').find_previous(class_='number')
page_number = int(page_number.text)
file_name = soup.find(class_='doctor-count')

with open(file_name.text.strip()+'.csv', 'w', encoding='utf-8', newline='') as csvfile:
    doctors_writer = csv.writer(csvfile, delimiter=',')
    doctors_writer.writerow(CSV_HEADER)
    for page in range (1, page_number+1):
        req = requests.get(URL+f'?pagenumber={page}')
        src = req.text
        with open('index.html', 'w', encoding='utf-8') as file:
           file.write(src)
        soup = BeautifulSoup(src, 'lxml')
        print(f'********** Doctors on page {page} *************')
        all_doctors = soup.find_all(class_='prov-name')

        for doctor in all_doctors:

            doctor_name = doctor.text
            doctor_link = doctor.get('href')
            print(f'{doctor_name}: {doctor_link}')

            each_doc_page = requests.get(doctor_link, HEADERS)
            src_2 = each_doc_page.text

            soup_2 = BeautifulSoup(src_2, 'lxml')
            clinic = soup_2.find(class_='prov-location-name loc-co-tplcnm')
            clinic_address = soup_2.find(class_='prov-address-text loc-co-tplcadd')
            contact_phone = soup_2.find(class_='webmd-button phone-btn loc-co-tpphn webmd-button--ghost webmd-button--medium is-round')



            record = ['','','','','']
            record[0] = doctor_name
            if clinic:
                record[1]=clinic.text.strip()
            if clinic_address:
                record[2]=clinic_address.text.strip()
            if contact_phone:
                record[3]=contact_phone.text.strip()
            record[4]=doctor_link
            doctors_writer.writerow(record)

