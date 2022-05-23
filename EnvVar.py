import os
# Set Environment Variables

def SetEnvVariables(email_option):
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
    
    return os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD']
