"""Provides utility functions for scraping."""

def normalize(s):
    """Trim the string to a standard format."""
    # Remove leading/trailing whitespace
    s = s.strip()
    # Remove trailing comma
    if s.endswith(","):
        s = s[:-1]

    return s
