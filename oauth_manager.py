"""
OAuth 2.0 authentication manager for Google and Microsoft calendar integration.
"""
import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import msal


# OAuth 2.0 scopes
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/calendar']
MICROSOFT_SCOPES = ['Calendars.ReadWrite']

# Token storage path
TOKEN_DIR = Path.home() / '.calendar_mcp_tokens'
TOKEN_DIR.mkdir(exist_ok=True)


class OAuthManager:
    """Manages OAuth 2.0 authentication for calendar providers."""
    
    def __init__(self):
        self.google_creds: Optional[Credentials] = None
        self.microsoft_token: Optional[Dict[str, Any]] = None
        
    def get_google_credentials(self) -> Optional[Credentials]:
        """
        Get Google OAuth 2.0 credentials.
        Returns cached credentials or initiates OAuth flow if needed.
        """
        token_path = TOKEN_DIR / 'google_token.json'
        creds = None
        
        # Load existing token
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), GOOGLE_SCOPES)
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Need credentials.json file with OAuth client config
                credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(
                        f"Google credentials file not found at {credentials_path}. "
                        "Please download OAuth 2.0 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, GOOGLE_SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next time
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.google_creds = creds
        return creds
    
    def get_microsoft_token(self) -> Optional[Dict[str, Any]]:
        """
        Get Microsoft OAuth 2.0 access token.
        Returns cached token or initiates OAuth flow if needed.
        """
        token_path = TOKEN_DIR / 'microsoft_token.json'
        
        # Load existing token
        if token_path.exists():
            with open(token_path, 'r') as f:
                token_data = json.load(f)
                self.microsoft_token = token_data
                return token_data
        
        # Get client credentials from environment
        client_id = os.getenv('MICROSOFT_CLIENT_ID')
        client_secret = os.getenv('MICROSOFT_CLIENT_SECRET')
        tenant_id = os.getenv('MICROSOFT_TENANT_ID', 'common')
        
        if not client_id or not client_secret:
            raise ValueError(
                "Microsoft credentials not found. Please set MICROSOFT_CLIENT_ID "
                "and MICROSOFT_CLIENT_SECRET environment variables."
            )
        
        # Create MSAL app
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = msal.PublicClientApplication(
            client_id,
            authority=authority
        )
        
        # Try to get token from cache
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(MICROSOFT_SCOPES, account=accounts[0])
            if result and 'access_token' in result:
                self.microsoft_token = result
                with open(token_path, 'w') as f:
                    json.dump(result, f)
                return result
        
        # Interactive login flow
        result = app.acquire_token_interactive(
            scopes=MICROSOFT_SCOPES,
            prompt='select_account'
        )
        
        if 'access_token' in result:
            self.microsoft_token = result
            with open(token_path, 'w') as f:
                json.dump(result, f)
            return result
        else:
            error = result.get('error_description', 'Unknown error')
            raise Exception(f"Failed to acquire Microsoft token: {error}")
    
    def logout_google(self) -> bool:
        """Remove stored Google credentials."""
        token_path = TOKEN_DIR / 'google_token.json'
        if token_path.exists():
            token_path.unlink()
            self.google_creds = None
            return True
        return False
    
    def logout_microsoft(self) -> bool:
        """Remove stored Microsoft credentials."""
        token_path = TOKEN_DIR / 'microsoft_token.json'
        if token_path.exists():
            token_path.unlink()
            self.microsoft_token = None
            return True
        return False
    
    def is_authenticated(self, provider: str) -> bool:
        """Check if authenticated with a specific provider."""
        if provider.lower() == 'google':
            token_path = TOKEN_DIR / 'google_token.json'
            return token_path.exists()
        elif provider.lower() == 'microsoft':
            token_path = TOKEN_DIR / 'microsoft_token.json'
            return token_path.exists()
        return False
