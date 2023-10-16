import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Base URL for the links in the RSS feed
base_url = "https://ramirogarcia.xyz"

# Read the existing RSS feed (if any) to check for duplicates
existing_items = set()

try:
    existing_xml = ET.parse("news_feed.xml")
    existing_root = existing_xml.getroot()
    for item in existing_root.findall(".//item"):
        title = item.findtext(".//title")
        existing_items.add(title)
except FileNotFoundError:
    pass  # If the XML file doesn't exist, ignore the exception

# Read the HTML content from the "index.html" file
with open("index.html", "r", encoding="utf-8") as html_file:
    html_content = html_file.read()

# Parse the HTML using Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find the "news" section
news_section = soup.find("section", {"id": "news"})

if news_section:
    # Create the root element for the RSS feed
    rss = ET.Element("rss", attrib={"version": "2.0"})

    # Create the channel element
    channel = ET.SubElement(rss, "channel")

    # Find and append new <li> items to the RSS feed
    for li in news_section.find("ul", class_="wip").find_all("li"):
        # Extract the content of the <li> element
        li_text = ' '.join([str(text) for text in li.contents if isinstance(text, str)])

        # Check if the item title already exists in the RSS feed
        if li_text not in existing_items:
            # Add the item to the existing items set and the RSS feed
            existing_items.add(li_text)
            
            # Check if the <li> contains an <a> tag with an 'href' attribute
            link_element = li.find("a", href=True)
            if link_element:
                # If a link is present, use it as the description
                description = link_element["href"]
            else:
                # If no link is present, use an empty string as the description
                description = ""
                
            item = ET.SubElement(channel, "item")
            item_title = ET.SubElement(item, "title")
            item_title.text = li_text
            
            item_description = ET.SubElement(item, "description")
            item_description.text = description

    # Create an XML tree and save it to a file
    xml_tree = ET.ElementTree(rss)
    xml_tree.write("news_feed.xml")

    print("New items appended to the RSS feed.")
else:
    print("No 'news' section found in the HTML.")
