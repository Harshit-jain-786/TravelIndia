from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .contactserializers import ContactMessageSerializer

class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Send confirmation email to user
            import smtplib
            from email.mime.text import MIMEText
            user_subject = "Enquiry Submitted - TravelIndia"
            user_body = "Dear {0},\n\nYour enquiry has been submitted successfully. We will get back to you soon!\n\nThank you for contacting TravelIndia.".format(contact.first_name)
            user_msg = MIMEText(user_body)
            user_msg['Subject'] = user_subject
            user_msg['From'] = 'hj1287091@gmail.com'
            user_msg['To'] = contact.email

            # Send notification email to admin
            admin_email = 'hj1287091@gmail.com'  # your email
            admin_subject = "New Contact Form Submission - TravelIndia"
            admin_body = f"New enquiry from {contact.first_name} {contact.last_name} ({contact.email}):\n\nSubject: {contact.subject}\nMessage: {contact.message}\nPhone: {contact.phone}"
            admin_msg = MIMEText(admin_body)
            admin_msg['Subject'] = admin_subject
            admin_msg['From'] = 'hj1287091@gmail.com'
            admin_msg['To'] = admin_email

            try:
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login('hj1287091@gmail.com', 'ffkf gkbi gxzq rxmd')
                smtp_server.sendmail('hj1287091@gmail.com', [contact.email], user_msg.as_string())
                smtp_server.sendmail('hj1287091@gmail.com', [admin_email], admin_msg.as_string())
                smtp_server.quit()
            except Exception as e:
                return Response({'error': 'Message saved but failed to send email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Message sent successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
