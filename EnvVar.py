import os
# Set Environment Variables

def SetEnvVariables(email_option:int):
    """_summary_

    Args:
        email_option (int): Selects the email id credentials for Outlook and Gmail

    Returns:
        _type_: Returns email credentials for yagmail.SMTP to send email
    """
    if email_option == 1:
        # Outlook Mail Details
        EMAIL_ID = os.environ['OUTLOOK_EMAIL']
        EMAIL_PASSWORD = os.environ['OUTLOOK_PASSWORD']
    
    elif email_option == 2:
        # GMail Details
        EMAIL_ID = os.environ['GMAIL_EMAIL']
        EMAIL_PASSWORD = os.environ['GMAIL_PASSWORD']
        
    else:
        print('Invalid Email Option')
    
    return (EMAIL_ID, EMAIL_PASSWORD)
