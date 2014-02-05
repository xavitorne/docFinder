"""Script to find doctor disponibility in apss trentino website."""

import sys
import requests
from bs4 import BeautifulSoup

base_url = "http://89.190.163.118/Pubblico/RicercaMedici/RicercaPerNomeMedico.rails"
search_url_base = "http://89.190.163.118/%s/Pubblico/RicercaMedici/RicercaPerNomeMedico.rails"
status_url_base = "http://89.190.163.118/%s/Pubblico/RicercaMedici/%s"


def get_cookie():
    """Get cookie from the site"""
    response = requests.get(base_url)
    cookie = response.url.split('/')[3]
    return cookie

def search_doctor(name, cookie):
    """Search list of doctors with that name"""
    query = {'richiesta.TipoRicerca': '1',
             'richiesta.TipoMedico': '1',
             'richiesta.NominativoMedico': name}
    search_url = search_url_base % cookie
    response = requests.post(search_url, data=query)

    soup = BeautifulSoup(response.text)
    doctor_list = soup.findAll('a', {'class': 'medico'})

    return doctor_list

def get_doctor_details(medico, cookie):
    """Get doctor details - not finished"""
    detail_link = medico.find('a').get('href')
    detail_link = status_url_base % (cookie, detail_link)
    response = requests.get(detail_link)
    soup = BeautifulSoup(response.text)
    table = soup.find('table')

    hours = [td for td in table.findAll('td')]

    i=0
    for th in table.findAll('th'):
        print th.string + " %s" % hours[i]
        i+=1

def get_doctor_status(lista, cookie, details=False):
    """Search status"""
    for link in lista:
        full_link = status_url_base % (cookie, link.get('href'))
        response = requests.get(full_link)
        soup = BeautifulSoup(response.text)
        medico = soup.find('div', {'class': 'medico-choice'})

        if details:
            get_doctor_details(medico, cookie)

        for td in medico.findAll('td'):
            if td.has_attr('class') and 'disponibilita' in td.get('class')[0]:
                return td.string

def main():
    """Main entry point for the script."""
    if len((sys.argv)) ==  1:
        print "Missing name! A name is required"
        return 0

    # Get cookie from the web
    cookie = get_cookie()

    name = sys.argv[1:][0]
    lista = search_doctor(name, cookie)
    status = get_doctor_status(lista, cookie, details=False)
    print "Status %s: %s" % (name, status)

if __name__ == '__main__':
    sys.exit(main())
