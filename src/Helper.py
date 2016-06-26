import re


def filter_entry_text(entry_text):
    regexp = re.compile(r'<div>')
    if regexp.search(entry_text) is not None and not entry_text.startswith('<div>'):
        entry_text = '<div>' + re.sub('<div>', '</div><div>', entry_text, 1)
    return entry_text