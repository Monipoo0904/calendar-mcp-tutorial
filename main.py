from mcp.server.fastmcp import FastMCP 
from typing import List, Dict 
from datetime import datetime
import os
import json

# Import new modules
from oauth_manager import OAuthManager
from calendar_api import CalendarAPI
from ics_generator import ICSGenerator

# Create an MCP server 
mcp = FastMCP("EventCalendar")

# Initialize managers
oauth_manager = OAuthManager()
calendar_api = CalendarAPI()
ics_generator = ICSGenerator() 


# In-memory storage for events 
# Each event is a dict: {"title": str, "date": str, "description": str} 
events: List[Dict] = [] 

# Add an event 
@mcp.tool() 

def add_event(title: str, date: str, description: str = "") -> str: 
  """ 
  Add a new calendar event. 
  Date format: YYYY-MM-DD 
  """ 
  try: 
    # Validate date format 
    datetime.strptime(date, "%Y-%m-%d") 
    events.append({"title": title, "date": date, "description": description}) 
    return f"Event '{title}' added for {date}." 
  except ValueError: 
    return "Invalid date format. Use YYYY-MM-DD." 
# View all events 
@mcp.tool() 

def view_events() -> str: 
  """ 
  Return all events in the calendar. 
  """ 
  if not events: 
    return "No events scheduled." 
  result = "Calendar Events:\n" 
  for event in sorted(events, key=lambda x: x["date"]): 
    desc = f" - {event['description']}" if event['description'] else "" 
    result += f"- {event['date']}: {event['title']}{desc}\n" 
  return result 
# Delete an event by title 
@mcp.tool() 

def delete_event(title: str) -> str: 
  """ 
  Delete an event by its title. 
  """ 
  initial_length = len(events) 
  events[:] = [e for e in events if e["title"].lower() != title.lower()] 
  if len(events) < initial_length: 
    return f"Event '{title}' deleted." 
  else: 
    return f"No event found with title '{title}'." 

# Summarize events 
@mcp.prompt() 
def summarize_events() -> str: 
  """
  Generate a summary of upcoming events. 
  """ 

  if not events: 
    return "No events scheduled." 
  summary = "Upcoming Events Summary:\n" 
  for e in sorted(events, key=lambda x: x["date"]): 
    summary += f"- {e['date']}: {e['title']}" 
    if e['description']: 
      summary += f" ({e['description']})" 
    summary += "\n" 
  return summary 

if __name__ == "__main__": 
  mcp.run()

# OAuth Login Tool
@mcp.tool()
def oauth_login(provider: str) -> str:
  """
  Authenticate with a calendar provider using OAuth 2.0.
  
  Args:
    provider: Calendar provider ('google' or 'microsoft')
  
  Returns:
    Authentication status message
  """
  provider = provider.lower()
  
  if provider not in ['google', 'microsoft']:
    return f"Unsupported provider: {provider}. Supported providers: google, microsoft"
  
  try:
    if provider == 'google':
      creds = oauth_manager.get_google_credentials()
      if creds and creds.valid:
        return f"Successfully authenticated with Google Calendar!"
      else:
        return "Failed to authenticate with Google Calendar. Please check credentials."
    
    elif provider == 'microsoft':
      token = oauth_manager.get_microsoft_token()
      if token and 'access_token' in token:
        return f"Successfully authenticated with Microsoft Outlook Calendar!"
      else:
        return "Failed to authenticate with Microsoft Calendar. Please check credentials."
  
  except FileNotFoundError as e:
    return f"Configuration error: {str(e)}"
  except ValueError as e:
    return f"Configuration error: {str(e)}"
  except Exception as e:
    return f"Authentication failed: {str(e)}"

# Check Authentication Status
@mcp.tool()
def check_auth_status(provider: str = "all") -> str:
  """
  Check authentication status for calendar providers.
  
  Args:
    provider: Provider to check ('google', 'microsoft', or 'all')
  
  Returns:
    Authentication status
  """
  provider = provider.lower()
  
  if provider == "all":
    google_status = "✓ Authenticated" if oauth_manager.is_authenticated('google') else "✗ Not authenticated"
    microsoft_status = "✓ Authenticated" if oauth_manager.is_authenticated('microsoft') else "✗ Not authenticated"
    return f"Authentication Status:\n- Google: {google_status}\n- Microsoft: {microsoft_status}"
  elif provider == "google":
    status = "✓ Authenticated" if oauth_manager.is_authenticated('google') else "✗ Not authenticated"
    return f"Google: {status}"
  elif provider == "microsoft":
    status = "✓ Authenticated" if oauth_manager.is_authenticated('microsoft') else "✗ Not authenticated"
    return f"Microsoft: {status}"
  else:
    return f"Unknown provider: {provider}. Use 'google', 'microsoft', or 'all'."

# Create Calendar Event
@mcp.tool()
def create_calendar_event(
  provider: str,
  title: str,
  date: str,
  description: str = "",
  start_time: str = "09:00",
  end_time: str = "10:00",
  timezone: str = "UTC"
) -> str:
  """
  Create an event in a calendar provider (Google or Microsoft).
  
  Args:
    provider: Calendar provider ('google' or 'microsoft')
    title: Event title
    date: Event date (YYYY-MM-DD)
    description: Event description (optional)
    start_time: Start time (HH:MM, default: 09:00)
    end_time: End time (HH:MM, default: 10:00)
    timezone: Timezone (default: UTC)
  
  Returns:
    Event creation status
  """
  provider = provider.lower()
  
  # Validate date format
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    return "Invalid date format. Use YYYY-MM-DD."
  
  # Validate time format
  try:
    datetime.strptime(start_time, "%H:%M")
    datetime.strptime(end_time, "%H:%M")
  except ValueError:
    return "Invalid time format. Use HH:MM (e.g., 09:00)."
  
  if provider == 'google':
    try:
      creds = oauth_manager.get_google_credentials()
      result = calendar_api.create_google_event(
        creds, title, date, description, start_time, end_time, timezone
      )
      
      if result['success']:
        return f"✓ Event created in Google Calendar!\nTitle: {title}\nDate: {date}\nLink: {result.get('link', 'N/A')}"
      else:
        return f"Failed to create Google Calendar event: {result.get('error', 'Unknown error')}"
    
    except Exception as e:
      return f"Error: {str(e)}. Please authenticate first using oauth_login tool."
  
  elif provider == 'microsoft':
    try:
      token = oauth_manager.get_microsoft_token()
      if not token or 'access_token' not in token:
        return "Not authenticated with Microsoft. Please use oauth_login tool first."
      
      result = calendar_api.create_microsoft_event(
        token['access_token'], title, date, description, start_time, end_time, timezone
      )
      
      if result['success']:
        return f"✓ Event created in Microsoft Outlook Calendar!\nTitle: {title}\nDate: {date}\nLink: {result.get('link', 'N/A')}"
      else:
        return f"Failed to create Microsoft Calendar event: {result.get('error', 'Unknown error')}"
    
    except Exception as e:
      return f"Error: {str(e)}. Please authenticate first using oauth_login tool."
  
  else:
    return f"Unsupported provider: {provider}. Supported providers: google, microsoft. For other providers, use export_ics tool."

# Export ICS File (Fallback)
@mcp.tool()
def export_ics(
  title: str,
  date: str,
  description: str = "",
  start_time: str = "09:00",
  end_time: str = "10:00",
  timezone: str = "UTC"
) -> str:
  """
  Generate an .ics file for manual import (fallback for unsupported providers).
  
  Args:
    title: Event title
    date: Event date (YYYY-MM-DD)
    description: Event description (optional)
    start_time: Start time (HH:MM, default: 09:00)
    end_time: End time (HH:MM, default: 10:00)
    timezone: Timezone (default: UTC)
  
  Returns:
    File path to generated .ics file
  """
  # Validate date format
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    return "Invalid date format. Use YYYY-MM-DD."
  
  # Validate time format
  try:
    datetime.strptime(start_time, "%H:%M")
    datetime.strptime(end_time, "%H:%M")
  except ValueError:
    return "Invalid time format. Use HH:MM (e.g., 09:00)."
  
  result = ics_generator.generate_ics(title, date, description, start_time, end_time, timezone)
  
  if result['success']:
    return f"✓ ICS file generated!\nFile: {result['file_path']}\nYou can import this file into any calendar application (Apple Calendar, Google Calendar, Outlook, etc.)."
  else:
    return f"Failed to generate ICS file: {result.get('error', 'Unknown error')}"

# Logout Tool
@mcp.tool()
def oauth_logout(provider: str) -> str:
  """
  Logout from a calendar provider.
  
  Args:
    provider: Calendar provider ('google' or 'microsoft')
  
  Returns:
    Logout status message
  """
  provider = provider.lower()
  
  if provider == 'google':
    if oauth_manager.logout_google():
      return "Successfully logged out from Google Calendar."
    else:
      return "Not currently logged in to Google Calendar."
  
  elif provider == 'microsoft':
    if oauth_manager.logout_microsoft():
      return "Successfully logged out from Microsoft Outlook Calendar."
    else:
      return "Not currently logged in to Microsoft Calendar."
  
  else:
    return f"Unknown provider: {provider}. Use 'google' or 'microsoft'." 

