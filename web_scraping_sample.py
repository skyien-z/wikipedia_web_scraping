import requests
import bs4
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import Counter

def make_sections_dict(wikipedia_link):
    '''
    Parses the HTML of a wikipedia link (passed in as a string) into a dictionary that 
    maps section titles to a list of content tags (primarily paragraph tags) 
    that correspond to it.
    '''
    page = requests.get(wikipedia_link)
    soup = BeautifulSoup(page.content, 'lxml')
    
    title_to_content_tags = {}
    sections = soup.find_all("span", class_="mw-headline")
    
    for i in range(len(sections)):           
        add_section_to_dict(sections[i], title_to_content_tags)
    
    return title_to_content_tags

def add_section_to_dict(span_title_tag, title_to_content_tags):
    '''
    Takes in a span_title_tag and maps all tags that succeed it up
    to the next h2_title_tag. This mapped data is added to the
    dictionary title_to_content_tags passed in.
    '''
    section_title = span_title_tag.string
    title_to_content_tags[section_title] = [] 
    
    h2_title_tag = span_title_tag.parent
    
    for tag in h2_title_tag.next_siblings:
        # Don't add strings or NavigableString object to list
        if not isinstance(tag, bs4.element.Tag):
            continue
        
        # Returns when we find the title tag for the next section
        if (tag.name == "h2" and tag.span != None and 
            tag.span.attrs["class"] == ["mw-headline"]):
                return

        title_to_content_tags[section_title].append(tag)

def print_hyperlinks(list_of_tags):
    '''
    Prints all hyperlinks in a list of tags (values of the title_to_content_tags dictionary) 
    passed in that correspond to a given Wikipedia section.
    '''
    for tag in list_of_tags:
        hyperlinks = tag.find_all("a")
        
        # skip paragraph if it has no hyperlinks
        if (hyperlinks == []):
            continue
        
        for link in hyperlinks:
            if link.has_attr("href"):
                print(wikipedia_link + str(link["href"]))

def print_frequent_words(list_of_tags):
    '''
    Prints the 5 most frequently used words that aren't stop words in each section.
    '''
    word_list = get_word_list(list_of_tags)
    print(Counter(word_list).most_common(5))

def get_word_list(list_of_tags):
    '''
    Compiles list of words in a section that aren't stop words from
    a list of tags.
    '''
    stop_word_list = list(stopwords.words('english'))
    section_content = []
    for tag in list_of_tags:
        for string in tag.stripped_strings:
            word_list = string.split()
            for word in word_list:
                if word not in stop_word_list:
                    section_content.append(word)
    return section_content

def print_sections(title_to_content_tags):
    for section in title_to_content_tags:
        # prints section title
        print("The title of this section is: " + str(section) + "\n")
        
        # prints most frequent words
        print("The top 5 most frequent non-stop words are: ")
        print_frequent_words(title_to_content_tags[section])        
        print()  
        
        # prints hyperlinks
        print("The hyperlinks in this section are: ")
        print_hyperlinks(title_to_content_tags[section])

        print("\n")

# main –– this is a sample wikipedia link that can be subsituted and modified
wikipedia_link = "https://en.wikipedia.org/wiki/Candy"
title_to_content_tags_dict = make_sections_dict(wikipedia_link)
print_sections(title_to_content_tags_dict)