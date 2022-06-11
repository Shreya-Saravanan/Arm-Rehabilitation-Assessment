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
        os.environ['EMAIL_USER'] = 'email@outlook.com'
        os.environ['EMAIL_PASSWORD'] = 'Outlook_Password'
    
    elif email_option == 2:
        # GMail Details
        os.environ['EMAIL_USER'] = 'email@gmail.com'
        os.environ['EMAIL_PASSWORD'] = 'GMail_App_Password'
        
    else:
        print('Invalid Email Option')
    
    return (os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD'])
