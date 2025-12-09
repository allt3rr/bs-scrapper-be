import requests
from bs4 import BeautifulSoup

def olx_scrapper(OLX_URL):
    offers = []
    offer_counter = 0
    page = 1
    hasMore = True

    while hasMore:
        url = f'{OLX_URL}&page={page}'
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, 'html.parser')  # <- tu tworzysz soup
        cards = soup.select('.jobs-ad-card')

        if len(cards) == 0:
            hasMore = False
            break

        for i, card in enumerate(cards):
            name_tag = card.select_one('h4')
            name = name_tag.get_text() if name_tag else None

            salary_tag = card.find('p', string=lambda s: s and 'zł' in s)
            salary = salary_tag.get_text() if salary_tag else None

            link_tag = card.find('a', href=lambda s: s and '/oferta/praca/' in s)
            link = link_tag['href'] if link_tag else None

            detailed_data = card.select('.css-w0dc4x')

            # bezpieczne sprawdzenie city
            city_tag = detailed_data[0].select('.css-jw5wnz') if detailed_data else []
            city = city_tag[0].get_text() if city_tag else None

            availability_tag = detailed_data[1].get_text() if len(detailed_data) > 1 else None
            contract_type_tag = detailed_data[2].get_text() if len(detailed_data) > 2 else None

            offers.append({
                "id": offer_counter,
                "name": name,
                "salary": salary,
                "link": "https://olx.pl" + link if link else None,
                "city": city,
                "availability": availability_tag,
                "contract_type": contract_type_tag,
            })

            offer_counter += 1

        page += 1

    return {"title": "OLX oferty pracy", 'count': str(len(offers)), "offers": offers}
