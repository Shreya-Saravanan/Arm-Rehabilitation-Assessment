import EnvVar
import yagmail

def MailSettings(email_option:int, mailing_list:list, subject:str, body:str):
    """SMTP Setup and Sending Email

    Args:
        - email_option (int): Select the Email ID used to setup the SMTP server
        - mailing_list (list[str]): List of mail recipients to send the email
        - subject (str): Subject of the Email
        - body (str): Message to be sent in the Email
    """
    user, app_password = EnvVar.SetEnvVariables(email_option)

    if email_option == 1:
        port = 587  # For starttls   
        host_server = "smtp.office365.com"
        
        try:
            yagmail.SMTP(user = user,
                password = app_password,
                host = host_server,
                port = port,
                smtp_starttls = True,
                smtp_ssl = False).send(to = mailing_list, subject = subject, contents = body)
            
            print('Email Sent Successfully using Outlook Mail')
        
        except:
            print('Email not sent successfully using Outlook Mail')
            
        
    elif email_option == 2:
        
        try:
            yagmail.SMTP(user = user, password = app_password).send(to = mailing_list, subject = subject, contents = body)
            
            print('Email Sent Successfully using Gmail')
        
        except:
            print('Email not sent Successfully using Gmail')
            
    else:
        print('Invalid Mail Settings!!!')
