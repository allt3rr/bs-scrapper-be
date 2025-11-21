def olx_scrapper(soup):
    offers = []

    cards = soup.select('.jobs-ad-card')
    for i, card in enumerate(cards):
        name_tag = card.select_one('h4')
        name = name_tag.get_text()

        salary_tag = card.find('p', string=lambda s: 'zł' in s)
        salary = salary_tag.get_text() if salary_tag else None

        link_tag = card.find('a', href=lambda s: s and '/oferta/praca/' in s)
        link = link_tag['href'] if link_tag else None

        offers.append({
            "id": i,
            "name": name,
            "salary": salary,
            "link": "https://olx.pl" + link
        })

    return {"title": "OLX oferty pracy", "offers": offers}