# communication/agora_utils.py
import time
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

try:
    from agora_token_builder import RtcTokenBuilder, RtmTokenBuilder
    AGORA_TOKEN_BUILDER_AVAILABLE = True
except ImportError:
    AGORA_TOKEN_BUILDER_AVAILABLE = False
    print("Warning: agora-token-builder not installed. Install with: pip install agora-token-builder")


# ---------------------------------------
# Generate RTC Token (Video / Audio Call)
# ---------------------------------------
def generate_rtc_token(channel_name, uid, expire_time=3600):
    app_id = settings.AGORA_APP_ID
    certificate = settings.AGORA_APP_CERTIFICATE

    if not app_id or not certificate:
        logger.error("Agora App ID or Certificate not set in settings.py")
        print("❌ Agora App ID or Certificate not set")
        return None
    
    if not AGORA_TOKEN_BUILDER_AVAILABLE:
        logger.error("agora-token-builder package not installed")
        print("❌ agora-token-builder package not installed")
        return None

    try:
        current_ts = int(time.time())
        expire_ts = current_ts + expire_time

        # Role 1 = Publisher (recommended for both caller and receiver)
        role = 1  

        token = RtcTokenBuilder.buildTokenWithUid(
            app_id,
            certificate,
            channel_name,
            int(uid),
            role,
            expire_ts
        )
        
        logger.info(f"✅ Generated RTC token for channel: {channel_name}, uid: {uid}")
        print(f"✅ Generated RTC token for channel: {channel_name}, uid: {uid}")
        
        if not token or token == '':
            logger.error("Token generation returned empty token")
            print("❌ Token generation returned empty token")
            return None
            
        return token
        
    except Exception as e:
        logger.error(f"Error generating RTC token: {str(e)}")
        print(f"❌ Error generating RTC token: {e}")
        return None


# ---------------------------------------
# Generate RTM Token (Chat / Messaging)
# ---------------------------------------
def generate_rtm_token(uid, expire_time=3600):
    app_id = settings.AGORA_APP_ID
    certificate = settings.AGORA_APP_CERTIFICATE

    if not app_id or not certificate:
        print("Warning: Agora App ID or Certificate not set in settings.py")
        return None
    
    if not AGORA_TOKEN_BUILDER_AVAILABLE:
        print("Warning: agora-token-builder package not installed")
        return None

    try:
        current_ts = int(time.time())
        expire_ts = current_ts + expire_time

        # Agora RTM Role → 1 means "RTM_USER"
        role = 1

        token = RtmTokenBuilder.buildToken(
            app_id,
            certificate,
            str(uid),      # must be string
            role,
            expire_ts      # privilegeExpiredTs
        )
        
        print(f"Generated RTM token for uid: {uid}")
        return token
        
    except Exception as e:
        print(f"Error generating RTM token: {e}")
        return None