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

        detailed_data = card.select('.css-w0dc4x')
        # print(detailed_data)

        city_tag = detailed_data[0].select('.css-jw5wnz')[0].get_text()
        city = city_tag if city_tag else None
        
        availability_tag = detailed_data[1].get_text()
        availability = availability_tag if availability_tag else None

        contract_type_tag = detailed_data[2].get_text()
        contract_type = contract_type_tag if contract_type_tag else None

        offers.append({
            "id": i,
            "name": name,
            "salary": salary,
            "link": "https://olx.pl" + link,
            "city": city,
            "availability": availability,
            "contract_type": contract_type,
        })

    return {"title": "OLX oferty pracy", "offers": offers}