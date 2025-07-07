# Twitter/X API Setup Guide

## Step 1: Get Twitter/X API Credentials

1. Go to https://developer.twitter.com/
2. Sign in with your Twitter/X account
3. Apply for a developer account if you don't have one
4. Create a new app/project
5. Get your API credentials:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Bearer Token
   - Access Token
   - Access Token Secret

## Step 2: Update the Script

Replace the placeholder values in `cointelegraph.py`:

```python
# Twitter/X API Configuration
TWITTER_BEARER_TOKEN = "your_actual_bearer_token_here"
TWITTER_API_KEY = "your_actual_api_key_here"
TWITTER_API_SECRET = "your_actual_api_secret_here"
TWITTER_ACCESS_TOKEN = "your_actual_access_token_here"
TWITTER_ACCESS_TOKEN_SECRET = "your_actual_access_token_secret_here"
```

## Step 3: Test the Integration

Run the script to test if the Twitter/X API integration works:

```bash
python3 cointelegraph.py
```

## Notes

- The script will automatically fall back to simulated tweets if the API is not configured
- Make sure your Twitter/X API has the necessary permissions for reading tweets
- The script searches for recent tweets related to crypto keywords
- Rate limits apply - the script respects Twitter's API limits

## Troubleshooting

If you get API errors:
1. Check your credentials are correct
2. Ensure your Twitter/X developer account is approved
3. Verify your app has the necessary permissions
4. Check if you've hit rate limits 