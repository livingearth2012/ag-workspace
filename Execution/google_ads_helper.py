import os
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google_auth_oauthlib.flow import InstalledAppFlow

# Allow insecure transport for manual OAuth flow on VPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Load environment variables from the .env file in the same directory
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

def get_client():
    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    developer_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    refresh_token = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")

    if not refresh_token:
        print("Refresh token not found. Starting OAuth flow...")
        # If no refresh token, we need to get one
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/adwords"],
            redirect_uri="http://localhost"
        )
        
        # Manual flow for headless environments
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        
        print("\n" + "="*60)
        print("ACTION REQUIRED: GOOGLE ADS AUTHENTICATION")
        print("="*60)
        print(f"1. Please visit this URL in your browser:\n\n{auth_url}\n")
        print("2. Approve the permissions.")
        print("3. After you approve, the browser will likely fail to load a localhost page.")
        print("4. COPY the entire URL from the address bar of that failed page and paste it here.")
        print("="*60 + "\n")
        
        response_url = input("Paste the full redirect URL here: ").strip()
        flow.fetch_token(authorization_response=response_url)
        creds = flow.credentials
        
        refresh_token = creds.refresh_token
        print(f"\n\nSUCCESS! Your Refresh Token is: {refresh_token}\n")
        print("Please add the following line to your .env file:")
        print(f"GOOGLE_ADS_REFRESH_TOKEN={refresh_token}\n\n")
        
        # Optionally update the .env automatically (risky with multiple keys, so we'll just print for now)
    
    config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "developer_token": developer_token,
        "refresh_token": refresh_token,
        "use_proto_plus": True
    }
    
    return GoogleAdsClient.load_from_dict(config)
