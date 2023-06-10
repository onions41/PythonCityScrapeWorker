import re


def get_meeting_type_name(meeting_page_url):
    if re.search("/phea", meeting_page_url, flags=re.I):
        return "Public Hearing"
    elif re.search("/regu", meeting_page_url, flags=re.I):
        return "Regular Council Meeting"
    elif re.search("/spec", meeting_page_url, flags=re.I):
        return "Special Council Meeting"
    elif re.search("/icre", meeting_page_url, flags=re.I):
        return "In-camera Meeting"
    elif re.search("/cfsc", meeting_page_url, flags=re.I):
        return "City Finance Standing Committee"
    elif re.search("/pspc", meeting_page_url, flags=re.I):
        return "Policy and Strategic Priorities Standing Committee"
    else:
        raise Exception("Could not determine the type of meeting from url")
