"""
Helper utility functions for the Company Research Agent system.
"""

import re
from typing import Any, Dict, List, Optional
from datetime import datetime


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Input text
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove special characters that might cause issues
    text = text.strip()
    
    return text


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL string
    
    Returns:
        True if valid URL, False otherwise
    """
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string
    
    Returns:
        True if valid email, False otherwise
    """
    if not email:
        return False
    
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))


def validate_year(year: Any) -> bool:
    """
    Validate year is reasonable.
    
    Args:
        year: Year value
    
    Returns:
        True if valid year, False otherwise
    """
    try:
        year_int = int(year)
        current_year = datetime.now().year
        return 1800 <= year_int <= current_year
    except (ValueError, TypeError):
        return False


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (basic validation).
    
    Args:
        phone: Phone number string
    
    Returns:
        True if valid phone, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it's mostly digits (allow + at start)
    phone_pattern = re.compile(r'^\+?\d{7,15}$')
    return bool(phone_pattern.match(cleaned))


def extract_number_from_string(text: str) -> Optional[float]:
    """
    Extract numeric value from string.
    
    Args:
        text: String containing number
    
    Returns:
        Extracted number or None
    """
    if not text:
        return None
    
    # Remove common separators
    cleaned = re.sub(r'[,$%]', '', str(text))
    
    # Try to extract number
    match = re.search(r'-?\d+\.?\d*', cleaned)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    
    return None


def is_null_or_empty(value: Any) -> bool:
    """
    Check if value is null, None, or empty.
    
    Args:
        value: Value to check
    
    Returns:
        True if null/empty, False otherwise
    """
    if value is None:
        return True
    
    if isinstance(value, str):
        return not value.strip()
    
    if isinstance(value, (list, dict)):
        return len(value) == 0
    
    return False


def safe_get(dictionary: Dict, key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary.
    
    Args:
        dictionary: Dictionary to get from
        key: Key to retrieve
        default: Default value if key not found
    
    Returns:
        Value or default
    """
    try:
        return dictionary.get(key, default)
    except (AttributeError, KeyError):
        return default


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
    
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Input text
    
    Returns:
        Word count
    """
    if not text:
        return 0
    return len(text.split())


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def percentage_to_float(percentage: str) -> Optional[float]:
    """
    Convert percentage string to float.
    
    Args:
        percentage: Percentage string (e.g., "15%", "15.5%")
    
    Returns:
        Float value or None
    """
    if not percentage:
        return None
    
    try:
        # Remove % sign and convert
        cleaned = str(percentage).replace('%', '').strip()
        return float(cleaned)
    except ValueError:
        return None


def validate_regex_pattern(value: str, pattern: str) -> bool:
    """
    Validate value against regex pattern.
    
    Args:
        value: Value to validate
        pattern: Regex pattern
    
    Returns:
        True if matches, False otherwise
    """
    if not value or not pattern:
        return False
    
    try:
        return bool(re.match(pattern, value))
    except re.error:
        return False