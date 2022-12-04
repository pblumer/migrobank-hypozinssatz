import requests, bs4, os, sys, pathlib
import pandas as pd
from datetime import datetime


url = 'https://www.migrosbank.ch/privatpersonen/hypotheken-kredite/hypotheken/festhypothek.html'
try:
    html       = requests.get(url).text
    document   = bs4.BeautifulSoup(html, 'html.parser')

    table    = document.find(id='festhypothek-zinsen-content-1')
    # print(table)
    table_data = table.tbody.find_all("tr")
    # print(table_data)
    
    mortgages = pd.DataFrame()
    for tr in table.find_all("tr"):
        # print(tr)
        td_array = tr.find_all("td", class_="Table--bodyCell")
        if len(td_array) > 0:

            data = {'log_date': [datetime.now().strftime('%Y-%m-%dT%H:%M:%S')], 'laufzeit': [td_array[0].text], 'zins': [float(td_array[2].text[:-1].replace(',', '.'))]}
            df = pd.DataFrame.from_dict(data, orient='columns')

            mortgages = pd.concat([mortgages, df], ignore_index=True)

    print(mortgages)

    app_path = str(pathlib.Path(__file__).parent.resolve())
    mortgages.to_csv(app_path + '/mortgages/mortgages_' + datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '.csv')



except requests.exceptions.ConnectionError:
    print("You've got problems with connection.", file=sys.stderr)

