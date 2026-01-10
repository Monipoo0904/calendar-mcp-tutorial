# Calendar MCP Server

A Model Context Protocol (MCP) server for managing calendar events with OAuth 2.0 support for Google Calendar and Microsoft Outlook Calendar. Provides fallback functionality with .ics file generation for unsupported calendar providers.

## Features

- 📅 **Multi-Provider Support**: Integrate with Google Calendar and Microsoft Outlook Calendar
- 🔐 **OAuth 2.0 Authentication**: Secure authentication using industry-standard OAuth 2.0
- 💾 **In-Memory Event Storage**: Store events locally for quick access
- 📥 **ICS File Export**: Generate .ics files for manual import into any calendar application
- 🛠️ **MCP Tools**: Expose calendar operations as MCP tools for AI assistants

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Monipoo0904/calendar-mcp-server.git
cd calendar-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv:
```bash
uv pip install -r requirements.txt
```

## Configuration

### Google Calendar Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials as `credentials.json`
6. Place `credentials.json` in the project root directory

### Microsoft Outlook Calendar Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" > "App registrations"
3. Register a new application
4. Add "Calendars.ReadWrite" permission
5. Create a client secret
6. Set environment variables:

```bash
export MICROSOFT_CLIENT_ID="your_client_id"
export MICROSOFT_CLIENT_SECRET="your_client_secret"
export MICROSOFT_TENANT_ID="common"  # or your tenant ID
```

Or create a `.env` file (see `.env.example`).

## Usage

### Running the Server

```bash
python main.py
```

### Available MCP Tools

#### 1. `oauth_login` - Authenticate with Calendar Provider
```json
{
  "tool": "oauth_login",
  "input": {
    "provider": "google"
  }
}
```

#### 2. `check_auth_status` - Check Authentication Status
```json
{
  "tool": "check_auth_status",
  "input": {
    "provider": "all"
  }
}
```

#### 3. `create_calendar_event` - Create Event in Calendar
```json
{
  "tool": "create_calendar_event",
  "input": {
    "provider": "google",
    "title": "Team Meeting",
    "date": "2026-01-15",
    "description": "Quarterly planning session",
    "start_time": "14:00",
    "end_time": "15:00",
    "timezone": "UTC"
  }
}
```

#### 4. `export_ics` - Generate ICS File (Fallback)
```json
{
  "tool": "export_ics",
  "input": {
    "title": "Team Meeting",
    "date": "2026-01-15",
    "description": "Quarterly planning session",
    "start_time": "14:00",
    "end_time": "15:00",
    "timezone": "UTC"
  }
}
```

#### 5. `oauth_logout` - Logout from Calendar Provider
```json
{
  "tool": "oauth_logout",
  "input": {
    "provider": "google"
  }
}
```

#### 6. Legacy Tools (In-Memory Storage)

- `add_event`: Add event to in-memory storage
- `view_events`: View all stored events
- `delete_event`: Delete event by title
- `summarize_events`: Get summary of events

## Architecture

```
calendar-mcp-server/
├── main.py              # MCP server and tool definitions
├── oauth_manager.py     # OAuth 2.0 authentication management
├── calendar_api.py      # Google and Microsoft Calendar API integration
├── ics_generator.py     # ICS file generation for fallback
├── api/
│   └── mcp.py          # Vercel serverless handler
├── pyproject.toml       # Project configuration
└── requirements.txt     # Python dependencies
```

## Security Considerations

- OAuth tokens are stored locally in `~/.calendar_mcp_tokens/`
- Never commit `credentials.json`, `.env`, or token files to version control
- Use environment variables for sensitive configuration
- Token files are automatically gitignored

## Fallback for Unsupported Providers

For calendar providers not directly supported (Apple Calendar, Yahoo Calendar, etc.), use the `export_ics` tool to generate an .ics file that can be manually imported into any calendar application.

## Dependencies

- `google-auth-oauthlib` - Google OAuth 2.0 authentication
- `google-api-python-client` - Google Calendar API
- `msal` - Microsoft Authentication Library
- `icalendar` - ICS file generation
- `python-dotenv` - Environment variable management

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
