### Beer fetching app ###

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import PySimpleGUI as sg

i = -1
beer_list = []
appended_beer_list = []

driver = webdriver.Chrome('G:/Beer Selection App/chromedriver')
print("Odota hetki. Haemme dataa Alkon kotisivuilta. Tämä saattaa kestää minuutin tai pari...")

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get(
    'https://www.alko.fi/tuotteet/tuotelistaus?SearchTerm=*&PageSize=12&SortingAttribute=&PageNumber=16&SearchParameter=%26%40QueryTerm%3D*%26ContextCategoryUUID%3DyW3AqHh4ul0AAAFVIGocppid%26OnlineFlag%3D1&SkipToId=product-tile-761235&SkipNextSeed=true')

driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

time.sleep(3)
previous_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    time.sleep(0.5)

    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == previous_height:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        lists = soup.find_all('div', class_="mini-card-wrap column")

        for list in lists:
            i += 1
            title = list.find("div", class_="mc-name hide-for-grid-view").text.replace('\n', '')
            description = list.find("div", class_="html-print").text.replace('\n', '')
            description_no_commas = description.replace(',', '-')
            description_no_dots = description_no_commas.replace('.', '')

            beer_data = [title, description_no_dots.lower()]
            beer_list.insert(i, beer_data)

        break
    previous_height = new_height

# Create one big list
for value in range(len(beer_list)):
    x = beer_list[value][1].split("-")
    y = [item.strip(' ') for item in x]
    for j in y:
        appended_beer_list.append(j)

nodup_desc_list = []
for element in appended_beer_list:
    if element not in nodup_desc_list:
        nodup_desc_list.append(element)

# HERE IS THE LIST BELOW FOR SORTED LIST WITH ALL DESCRIPTIONS. CAN BE USED IN GUI.
sort_nodup_list = sorted(nodup_desc_list)

sg.theme('LightBrown4')
# All the stuff inside your window
layout = [[sg.Text('Valitse myymälä: ')],
          [sg.Text('                           ')],
          [sg.Text('Anna haluttu olutkuvaus 1: '), sg.DD(sort_nodup_list, default_value=sort_nodup_list[0])],
          [sg.Text('Anna haluttu olutkuvaus 2: '), sg.DD(sort_nodup_list, default_value=sort_nodup_list[0])],
          [sg.Text('Anna haluttu olutkuvaus 3: '), sg.DD(sort_nodup_list, default_value=sort_nodup_list[0])],
          [sg.Text('Anna haluttu olutkuvaus 4: '), sg.DD(sort_nodup_list, default_value=sort_nodup_list[0])],
          [sg.Text('Anna haluttu olutkuvaus 5: '), sg.DD(sort_nodup_list, default_value=sort_nodup_list[0])],
          [sg.Button('Hae'), sg.Button('Sulje')]]

# Create the Window
window = sg.Window('Oluiden suositusohjelma', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Sulje':  # if user closes window or clicks cancel
        break
    comp_value_one = values[0]
    comp_value_two = values[1]
    comp_value_three = values[2]
    comp_value_four = values[3]
    comp_value_five = values[4]

    user_choises = [comp_value_one, comp_value_two, comp_value_three, comp_value_four, comp_value_five]

    # STRING-MATCHING (Compare user choices with beer list and give percentage for matching)
    # Go through first line and compare if matching word out of 5
    result_set_list = beer_list

    for i in range(len(beer_list)):
        points = 0
        for j in range(len(user_choises)):
            if user_choises[j] in beer_list[i][1] and user_choises[j] != '':
                points += 1

        result_set_list[i].append(str(points))


    result_set_list.sort(key=lambda x: x[2])
    #print(result_set_list[-10:])
    for rows in range(len(beer_list)):
        del result_set_list[rows][2]

    output = ""
    #print(result_set_list[-10:])
    top_list = result_set_list[-10:]
    for row in range(len(top_list)):
        output += (top_list[row][0]) + "\n"
    print(output)
    sg.PopupScrolled(output, title='Suosittelemamme oluet')










# Improvement Ideas
#   1. Add link to product on Alko
#   2. Add myymäläsaatavuus --> hämta html för varje sida, beautiful souppa myymäläsaatavuus o loopa den (adda som tredje column me titel + desc)
#   3. Kan man få de så att de bara e olutkuvaus fö de ölen som finns i en viss butik?
window.close()
