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


def coupon_extract_idc(start_position=0, end_position=0, html=""):
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


async def extract(session, urls):
    # Take udemy link and extract elements like stars, language, img ecc ecc
    udemy_element = []
    cont = await fetch.get_all(session, urls)
    if cont:
        for i, html in enumerate(cont):  # type: ignore
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
            # photo_course = soup.select(
            # "span.intro-asset--img-aspect--1UbeZ img")[0].get("src")
            subtitle = soup.find(
                "div", class_="udlite-text-md clp-lead__headline")

            if not language or not student or not stars or not num_ratings or not title_course or not subtitle or banner_error:  # or not photo_course
                continue
            if language.get_text() != "English":
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
