

prompt_template = """Given the text, identify and extract phone numbers, order numbers, and email addresses. Modify phone numbers that start with 0 by adding a prefix of 6 before you return them.

Phone Numbers can appear in the following formats:
601110019992
60123456789
0123456789 (This should be returned as 60123456789)
01110019992 (This should be returned as 601110019992)
011 1001999 1 (This should be returned as 60111001991)
012-3456789 (This should be returned as 6012-3456789

Order Numbers typically begin with any two alphabets (case insensitive) followed by numbers like:                    
AB2023082012345
XY202308210123

Email Addresses generally have the format:
localpart@domain.com

If you detect any of these entities, return them in the following JSON format:
{
phone: 'detected_phone_number',
order_no: 'detected_order_number',
email: 'detected_email_address'
}
If you don't detect any of the entities, return an empty JSON.
"""