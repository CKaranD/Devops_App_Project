import os
from end_of_topic_detector import EOT_checker

def lambda_end_of_topic(customer_input):
    # Set MPLCONFIGDIR to /tmp
    # os.environ['MPLCONFIGDIR'] = '/tmp'    
    
    eot_yes_no = EOT_checker(customer_input)

    return eot_yes_no
