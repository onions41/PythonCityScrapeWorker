import re, logging


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
    elif re.search("/nom", meeting_page_url, flags=re.I):
        return "Nomination Subcommittee"
    elif re.search("/agc", meeting_page_url, flags=re.I):
        return "Auditor General Committee"
    elif re.search("/agrc", meeting_page_url, flags=re.I):
        return "Auditor General Recruitment Committee"
    elif re.search("/blhe", meeting_page_url, flags=re.I):
        return "Business License Hearing"
    elif re.search("/crev", meeting_page_url, flags=re.I):
        return "Court of Revision"
    elif re.search("/inau", meeting_page_url, flags=re.I):
        return "Inaugural Council Meeting"
    else:
        logging.warning("Unrecognized meeting abbreviation for meeting url: %s. Labeled it Public Hearing anyway." % meeting_page_url)
        return "Public Hearing"
