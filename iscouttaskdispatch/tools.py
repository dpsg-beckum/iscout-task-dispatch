from datetime import datetime as dt
import re


def formatDatetime(timestamp: dt) -> str:
    return timestamp.strftime("%H:%M:%S") if timestamp.date() == dt.today().date() else timestamp.strftime("%d.%m.%Y %H:%M:%S")


def convert_text_to_links(text):
    # Regular expression to match URLs
    url_pattern = r'(https?://[^\s]+)'
    # Replacement pattern to convert URL to a clickable link
    replacement_pattern = r'<a href="\1" target="_blank">[Link: \1]</a>'

    # Replace URLs in the text with anchor tags
    converted_text = re.sub(url_pattern, replacement_pattern, text)
    
    return converted_text.replace("\r", "").replace("\n","<br>")

