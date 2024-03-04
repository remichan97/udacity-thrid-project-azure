import azure.functions as func
import logging
import os
from db_client import DbClient
from datetime import datetime
from sendgrid import Mail, SendGridAPIClient


app = func.FunctionApp()

@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="notificationqueue",
                               connection="techconf_SERVICEBUS") 
def servicebus_queue_trigger(azservicebus: func.ServiceBusMessage):
    notification_id = int(azservicebus.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    client = DbClient()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        notification = client.get_notification(notification_id=notification_id)
        # TODO: Get attendees email and name
        attendee = client.get_attendee()
        # TODO: Loop through each attendee and send an email with a personalized subject
        count = __send_email(notification, attendee)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        client.update_notification(notification_id=notification_id, complete_date=datetime.utcnow(), count=count)
    except (Exception) as error:
        logging.error(error)
    finally:
        client.close_connection()

def __send_email(notification, attendee):
    for row in attendee:
        message = Mail(
            from_email=os.getenv("SENDGRID_SEND_FROM"),
            to_emails=row[5],
            subject=notification[5],
            plain_text_content=notification[2])

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    return len(attendee)
