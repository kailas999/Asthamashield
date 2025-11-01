"""
Notification service for AsthmaShield
Handles SMS, email, and push notifications for asthma risk alerts
"""

import os
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        """Initialize notification service with AWS credentials"""
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        self.sns_client = None
        self.location_client = None
        
        # Initialize AWS clients if credentials are available
        if self.aws_access_key and self.aws_secret_key:
            try:
                self.sns_client = boto3.client(
                    'sns',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.aws_region
                )
                self.location_client = boto3.client(
                    'location',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key,
                    region_name=self.aws_region
                )
            except Exception as e:
                logger.error(f"Failed to initialize AWS clients: {e}")
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        # SMS configuration (Twilio)
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.twilio_client = None
        
        if self.twilio_account_sid and self.twilio_auth_token:
            try:
                self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")

    def send_email_alert(self, recipient_email, subject, message):
        """Send email alert for high asthma risk"""
        try:
            if not (self.smtp_server and self.email_user and self.email_password):
                logger.warning("Email configuration incomplete")
                return False
                
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_user, recipient_email, text)
            server.quit()
            
            logger.info(f"Email alert sent to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

    def send_sms_alert(self, phone_number, message):
        """Send SMS alert for high asthma risk"""
        try:
            if self.twilio_client:
                message = self.twilio_client.messages.create(
                    body=message,
                    from_=self.twilio_phone_number,
                    to=phone_number
                )
                logger.info(f"SMS alert sent to {phone_number}")
                return True
            elif self.sns_client:
                response = self.sns_client.publish(
                    PhoneNumber=phone_number,
                    Message=message
                )
                logger.info(f"SMS alert sent via SNS to {phone_number}")
                return True
            else:
                logger.warning("No SMS service configured")
                return False
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
            return False

    def send_push_notification(self, device_token, title, message):
        """Send push notification (stub implementation)"""
        try:
            # This would integrate with Firebase, APNs, or another push service
            # For now, we'll log the notification
            logger.info(f"Push notification to {device_token}: {title} - {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False

    def find_nearest_medical_facility(self, latitude, longitude, max_results=5):
        """Find nearest medical facilities using AWS Location Service"""
        try:
            if not self.location_client:
                logger.warning("AWS Location Service not configured")
                return []
            
            # This is a simplified implementation
            # In a real scenario, you would have a place index with medical facilities
            response = self.location_client.search_place_index_for_position(
                IndexName='medical-facilities-index',  # This would need to be created
                Position=[longitude, latitude],
                MaxResults=max_results
            )
            
            facilities = []
            for result in response.get('Results', []):
                place = result.get('Place', {})
                facilities.append({
                    'name': place.get('Label', 'Medical Facility'),
                    'address': place.get('AddressNumber', '') + ' ' + place.get('Street', ''),
                    'distance': result.get('Distance', 0),
                    'position': result.get('Position', [])
                })
            
            return facilities
        except Exception as e:
            logger.error(f"Failed to find nearest medical facility: {e}")
            return []

    def send_asthma_alert(self, user_info, risk_level, environmental_data):
        """Send comprehensive asthma alert with all notification methods"""
        try:
            # Create alert message
            message = self._create_alert_message(user_info, risk_level, environmental_data)
            subject = f"Asthma Risk Alert: {risk_level} Risk Detected"
            
            # Send email if email is provided
            if user_info.get('email'):
                self.send_email_alert(user_info['email'], subject, message)
            
            # Send SMS if phone number is provided
            if user_info.get('phone'):
                sms_message = f"Asthma Risk Alert: {risk_level} risk in your area. {environmental_data.get('pm25', 'N/A')} μg/m³ PM2.5."
                self.send_sms_alert(user_info['phone'], sms_message)
            
            # Send push notification if device token is provided
            if user_info.get('device_token'):
                self.send_push_notification(user_info['device_token'], subject, message)
                
            return True
        except Exception as e:
            logger.error(f"Failed to send asthma alert: {e}")
            return False

    def _create_alert_message(self, user_info, risk_level, environmental_data):
        """Create detailed alert message"""
        message = f"""
Asthma Risk Alert for {user_info.get('name', 'User')}

Risk Level: {risk_level}
Location: {user_info.get('city', 'Unknown')}

Environmental Conditions:
- PM2.5: {environmental_data.get('pm25', 'N/A')} μg/m³
- PM10: {environmental_data.get('pm10', 'N/A')} μg/m³
- Temperature: {environmental_data.get('temperature', 'N/A')}°C
- Humidity: {environmental_data.get('humidity', 'N/A')}%
- Pollen Level: {environmental_data.get('pollen_level', 'N/A')}

Recommendations:
1. Stay indoors during peak pollution hours
2. Keep windows closed
3. Use air purifier if available
4. Take prescribed medication as scheduled
5. Carry rescue inhaler

Nearest Medical Facilities:
"""
        
        # Add nearest medical facilities if location is available
        if user_info.get('latitude') and user_info.get('longitude'):
            facilities = self.find_nearest_medical_facility(
                user_info['latitude'], 
                user_info['longitude']
            )
            if facilities:
                for facility in facilities[:3]:  # Top 3 facilities
                    message += f"- {facility['name']} ({facility['distance']:.1f} km away)\n"
            else:
                message += "Unable to locate nearby medical facilities.\n"
        
        message += "\nFor immediate medical assistance, call emergency services."
        
        return message

# Global notification service instance
notification_service = NotificationService()

def send_asthma_alert(user_info, risk_level, environmental_data):
    """Convenience function to send asthma alert"""
    return notification_service.send_asthma_alert(user_info, risk_level, environmental_data)

def send_medication_reminder(user_info, medication_name, dosage_time):
    """Send medication reminder"""
    try:
        message = f"Medication Reminder: Time to take {medication_name} ({dosage_time})"
        
        # Send email reminder
        if user_info.get('email'):
            notification_service.send_email_alert(
                user_info['email'], 
                "Medication Reminder", 
                message
            )
        
        # Send SMS reminder
        if user_info.get('phone'):
            notification_service.send_sms_alert(user_info['phone'], message)
            
        # Send push notification
        if user_info.get('device_token'):
            notification_service.send_push_notification(
                user_info['device_token'], 
                "Medication Reminder", 
                message
            )
            
        return True
    except Exception as e:
        logger.error(f"Failed to send medication reminder: {e}")
        return False