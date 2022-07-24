from urllib.parse import unquote

from bs4 import BeautifulSoup
import fetch


def coupon_extract(start_position=0, end_position=0, html=""):
    coupon_position = html.find("couponCode")

    if coupon_position == -1:
        return

    # looking for the first character of the link "
    for i in range(coupon_position, -1, -1):
        if html[i] == '"':
            start_position = i+1
            break

    # Looking for the last character of the link "
    end_position = html.find('"', start_position)

    # better we unquote the string
    link_udemy = unquote(html[start_position:end_position])

    # remove "/" before ?couponCode
    slash_index = link_udemy.find("?couponCode")-1
    if (link_udemy[slash_index] == "/"):
        link_udemy = link_udemy[:slash_index] + link_udemy[slash_index+1:]

    return link_udemy


def coupon_extract_idc(start_position=0, end_position=0, html="") -> set:
    # example link: ...ulp=https://www.udemy.com/course/java-io-tutorial-for-beginners?couponCode=EDUCBA3..."
    # We found the common string couponCode and from there we iterate until we found the beginning and
    # the end of the string

    links_udemy = set()
    while ((coupon_position := html.find("couponCode", end_position)) != -1):
        # looking for the first character of the link =
        for i in range(coupon_position, -1, -1):
            if html[i] == '=':
                start_position = i+1
                break
        # Looking for the last character of the link "
        end_position = html.find('"', start_position)

    # better we unquote the string
        link_udemy = unquote(html[start_position:end_position])

        # remove "/" before ?couponCode
        slash_index = link_udemy.find("?couponCode")-1
        if (link_udemy[slash_index] == "/"):
            link_udemy = link_udemy[:slash_index] + link_udemy[slash_index+1:]

        links_udemy.add(link_udemy)
    return links_udemy


async def extract(session, urls) -> list:
    # Take udemy link and extract elements like stars, language, img ecc ecc
    # return list of dict with all this elements

    headers = {
        "Host": "www.udemy.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    udemy_element = []
    cont = []
    for url in urls:
        cont.append(await fetch.get(session, url, headers=headers))
    if cont is not None:
        for i, html in enumerate(cont):
            if html is not None:
                soup = BeautifulSoup(html, 'html.parser')
                title_course = soup.find(
                    "h1", class_="udlite-heading-xl clp-lead__title clp-lead__title--small")
                banner_error = soup.findAll(
                    "div", class_="alert-banner--text-frame--ZMG8W")
                language = soup.find(
                    "div", class_="clp-lead__element-item clp-lead__locale")
                student = soup.find("div", {"class": "enrollment"})
                stars = soup.find("span", {"data-purpose": "rating-number"})
                num_ratings = soup.find("a", {"data-purpose": "rating"})
                subtitle = soup.find(
                    "div", class_="udlite-text-md clp-lead__headline")

                if not language or not student or not stars or not num_ratings or not title_course or not subtitle or banner_error:
                    continue
                if language.get_text() != "Inglese":
                    continue

                # PREPARE elements
                num_ratings = num_ratings.get_text()
                num_ratings = num_ratings[num_ratings.find("(")+1:-1]
                udemy_element.append({"url": urls[i],
                                      "title": title_course.get_text(),
                                      "subtitle": subtitle.get_text(),
                                      "stars": stars.get_text(),
                                      "tot_rating": num_ratings,
                                      "students": student.get_text(),
                                      # "photo_url": photo_course,
                                      "language": language.get_text()
                                      })
    return udemy_element
