from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class UserListCreateView(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class RegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		import random, smtplib
		from email.mime.text import MIMEText
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			otp = str(random.randint(100000, 999999))
			user = serializer.save(
				password=request.data['password'],
				first_name=request.data.get('first_name', ''),
				last_name=request.data.get('last_name', ''),
				is_verified=False,
				otp_code=otp
			)

			# Send OTP via SMTP
			subject = "Your OTP Code"
			body = f"Your OTP code is: {otp}"
			msg = MIMEText(body)
			msg['Subject'] = subject
			msg['From'] = 'hj1287091@gmail.com'
			msg['To'] = user.email

			try:
				smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
				smtp_server.starttls()
				smtp_server.login('hj1287091@gmail.com', 'ffkf gkbi gxzq rxmd')# Replace with your email and password 
				smtp_server.sendmail('hj1287091@gmail.com', [user.email], msg.as_string())
				smtp_server.quit()
			except Exception as e:
				return Response({'error': 'Failed to send OTP', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

			return Response({'message': 'OTP sent to email. Please verify.'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VerifyOTPView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		email = request.data.get('email')
		otp = request.data.get('otp')
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
		if user.otp_code == otp:
			user.is_verified = True
			user.otp_code = ''
			user.save()

			# Send congratulatory email after successful verification
			import smtplib
			from email.mime.text import MIMEText
			subject = "Congratulations! Account Created"
			body = "Congratulations! Your account is created at TravelIndia."
			msg = MIMEText(body)
			msg['Subject'] = subject
			msg['From'] = 'hj1287091@gmail.com'
			msg['To'] = user.email
			try:
				smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
				smtp_server.starttls()
				smtp_server.login('hj1287091@gmail.com', 'ffkf gkbi gxzq rxmd')
				smtp_server.sendmail('hj1287091@gmail.com', [user.email], msg.as_string())
				smtp_server.quit()
			except Exception as e:
				return Response({'error': 'Account created but failed to send congratulatory email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

			return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
		return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'No account found with this email'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_verified:
            return Response(
                {'error': 'Email not verified'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Send login notification email in background (don't block response)
        try:
            import smtplib
            from email.mime.text import MIMEText
            from threading import Thread

            def send_notification_email():
                try:
                    subject = "Account Login Notification"
                    body = "Your account is logged in at TravelIndia. If this wasn't you, please secure your account."
                    msg = MIMEText(body)
                    msg['Subject'] = subject
                    msg['From'] = 'hj1287091@gmail.com'
                    msg['To'] = user.email
                    
                    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                    smtp_server.starttls()
                    smtp_server.login('hj1287091@gmail.com', 'ffkf gkbi gxzq rxmd')
                    smtp_server.sendmail('hj1287091@gmail.com', [user.email], msg.as_string())
                    smtp_server.quit()
                except Exception as e:
                    print(f"Failed to send login notification: {str(e)}")

            Thread(target=send_notification_email).start()
        except Exception as e:
            print(f"Failed to start notification thread: {str(e)}")

        response = Response({
            'refresh': str(refresh),
            'access': access_token,
            'user': UserSerializer(user).data
        })

        # Set httpOnly cookies
        response.set_cookie(
            'refresh_token',
            str(refresh),
            httponly=True,
            secure=True,
            samesite='Strict'
        )
        response.set_cookie(
            'access_token',
            access_token,
            httponly=True,
            secure=True,
            samesite='Strict'
        )

        return response

class ForgotPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        import random, smtplib
        from email.mime.text import MIMEText
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        otp = str(random.randint(100000, 999999))
        user.otp_code = otp
        user.save()
        subject = "Password Reset OTP - TravelIndia"
        body = f"Your OTP for password reset is: {otp}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'hj1287091@gmail.com'
        msg['To'] = user.email
        try:
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login('hj1287091@gmail.com', 'ffkf gkbi gxzq rxmd')
            smtp_server.sendmail('hj1287091@gmail.com', [user.email], msg.as_string())
            smtp_server.quit()
        except Exception as e:
            return Response({'error': 'Failed to send OTP', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'OTP sent to email for password reset.'}, status=status.HTTP_200_OK)

class ForgotPasswordVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        if not (email and otp and new_password):
            return Response({'error': 'Email, OTP, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp_code == otp:
            user.set_password(new_password)
            user.otp_code = ''
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
