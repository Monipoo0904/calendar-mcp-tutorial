"""
ICS file generator for calendar events (fallback for unsupported providers).
"""
from datetime import datetime, timedelta
from icalendar import Calendar, Event as ICalEvent
from typing import Dict
import os
from pathlib import Path


class ICSGenerator:
    """Generates .ics files for calendar events."""
    
    def __init__(self, output_dir: str = "/tmp/calendar_events"):
        """
        Initialize ICS generator.
        
        Args:
            output_dir: Directory to store generated .ics files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_ics(
        self,
        title: str,
        date: str,
        description: str = "",
        start_time: str = "09:00",
        end_time: str = "10:00",
        timezone: str = "UTC"
    ) -> Dict:
        """
        Generate an .ics file for a calendar event.
        
        Args:
            title: Event title
            date: Event date in YYYY-MM-DD format
            description: Event description
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
            timezone: Timezone identifier
        
        Returns:
            Dict with file path and event details
        """
        try:
            # Create calendar
            cal = Calendar()
            cal.add('prodid', '-//Calendar MCP Server//EN')
            cal.add('version', '2.0')
            
            # Create event
            event = ICalEvent()
            event.add('summary', title)
            event.add('description', description)
            
            # Parse datetime
            start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
            
            event.add('dtstart', start_dt)
            event.add('dtend', end_dt)
            event.add('dtstamp', datetime.now())
            
            # Add unique ID
            uid = f"{date}-{title.replace(' ', '-')}-{datetime.now().timestamp()}@calendar-mcp"
            event.add('uid', uid)
            
            # Add event to calendar
            cal.add_component(event)
            
            # Generate filename
            safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
            filename = f"{date}_{safe_title}.ics"
            filepath = self.output_dir / filename
            
            # Write to file
            with open(filepath, 'wb') as f:
                f.write(cal.to_ical())
            
            return {
                'success': True,
                'provider': 'ics',
                'file_path': str(filepath),
                'filename': filename,
                'title': title,
                'date': date,
                'message': f"ICS file created: {filepath}"
            }
        except Exception as e:
            return {
                'success': False,
                'provider': 'ics',
                'error': str(e)
            }
    
    def generate_ics_from_event(self, event: Dict) -> Dict:
        """
        Generate an .ics file from an event dictionary.
        
        Args:
            event: Dictionary with keys: title, date, description
        
        Returns:
            Dict with file path and event details
        """
        return self.generate_ics(
            title=event.get('title', 'Untitled Event'),
            date=event.get('date', datetime.now().strftime('%Y-%m-%d')),
            description=event.get('description', ''),
            start_time=event.get('start_time', '09:00'),
            end_time=event.get('end_time', '10:00'),
            timezone=event.get('timezone', 'UTC')
        )
