"""
Calendar API integration for Google Calendar and Microsoft Outlook.
"""
from typing import Dict, Optional
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests


class CalendarAPI:
    """Handles calendar operations for different providers."""
    
    def __init__(self):
        pass
    
    def create_google_event(
        self,
        credentials: Credentials,
        title: str,
        date: str,
        description: str = "",
        start_time: str = "09:00",
        end_time: str = "10:00",
        timezone: str = "UTC"
    ) -> Dict:
        """
        Create an event in Google Calendar.
        
        Args:
            credentials: Google OAuth credentials
            title: Event title
            date: Event date in YYYY-MM-DD format
            description: Event description
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            timezone: Timezone identifier (e.g., 'America/New_York')
        
        Returns:
            Dict with event details
        """
        try:
            service = build('calendar', 'v3', credentials=credentials)
            
            # Parse date and time
            start_datetime = f"{date}T{start_time}:00"
            end_datetime = f"{date}T{end_time}:00"
            
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': timezone,
                },
            }
            
            created_event = service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            return {
                'success': True,
                'provider': 'google',
                'event_id': created_event.get('id'),
                'link': created_event.get('htmlLink'),
                'title': title,
                'date': date
            }
        except Exception as e:
            return {
                'success': False,
                'provider': 'google',
                'error': str(e)
            }
    
    def create_microsoft_event(
        self,
        access_token: str,
        title: str,
        date: str,
        description: str = "",
        start_time: str = "09:00",
        end_time: str = "10:00",
        timezone: str = "UTC"
    ) -> Dict:
        """
        Create an event in Microsoft Outlook Calendar.
        
        Args:
            access_token: Microsoft OAuth access token
            title: Event title
            date: Event date in YYYY-MM-DD format
            description: Event description
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            timezone: Timezone identifier (e.g., 'Eastern Standard Time')
        
        Returns:
            Dict with event details
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            # Parse date and time
            start_datetime = f"{date}T{start_time}:00"
            end_datetime = f"{date}T{end_time}:00"
            
            event = {
                'subject': title,
                'body': {
                    'contentType': 'Text',
                    'content': description
                },
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': timezone
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': timezone
                }
            }
            
            response = requests.post(
                'https://graph.microsoft.com/v1.0/me/events',
                headers=headers,
                json=event
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    'success': True,
                    'provider': 'microsoft',
                    'event_id': result.get('id'),
                    'link': result.get('webLink'),
                    'title': title,
                    'date': date
                }
            else:
                return {
                    'success': False,
                    'provider': 'microsoft',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                'success': False,
                'provider': 'microsoft',
                'error': str(e)
            }
