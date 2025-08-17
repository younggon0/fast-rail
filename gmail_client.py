import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any
import os
from datetime import datetime
import re

class GmailClient:
    def __init__(self, email_address: str, app_password: str):
        self.email_address = email_address
        self.app_password = app_password
        self.imap = None
    
    def connect(self):
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.imap.login(self.email_address, self.app_password)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fetch_recent_emails(self, limit: int = 200) -> List[Dict[str, Any]]:
        if not self.imap:
            return []
        
        emails = []
        try:
            self.imap.select("INBOX")
            
            result, data = self.imap.search(None, "ALL")
            if result != "OK":
                return []
            
            email_ids = data[0].split()
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            email_ids.reverse()
            
            for email_id in email_ids:
                result, data = self.imap.fetch(email_id, "(RFC822)")
                if result != "OK":
                    continue
                
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                subject = self._decode_header(msg["Subject"])
                sender = self._decode_header(msg["From"])
                date_str = msg["Date"]
                
                try:
                    date_parsed = email.utils.parsedate_to_datetime(date_str)
                    date_formatted = date_parsed.strftime("%Y-%m-%d %H:%M")
                except:
                    date_formatted = date_str
                
                body = self._get_email_body(msg)
                
                emails.append({
                    "id": email_id.decode(),
                    "subject": subject,
                    "from": sender,
                    "date": date_formatted,
                    "body": body[:500],
                    "full_body": body
                })
            
            return emails
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def _decode_header(self, header):
        if not header:
            return ""
        decoded = decode_header(header)
        result = []
        for part, encoding in decoded:
            if isinstance(part, bytes):
                try:
                    result.append(part.decode(encoding or 'utf-8', errors='ignore'))
                except:
                    result.append(str(part))
            else:
                result.append(str(part))
        return " ".join(result)
    
    def _get_email_body(self, msg):
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        body = payload.decode(charset, errors='ignore')
                        break
                    except:
                        continue
        else:
            try:
                payload = msg.get_payload(decode=True)
                charset = msg.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='ignore')
            except:
                body = str(msg.get_payload())
        
        body = re.sub(r'<[^>]+>', '', body)
        body = re.sub(r'\s+', ' ', body)
        return body.strip()
    
    def archive_emails(self, email_ids: List[str]) -> Dict[str, Any]:
        if not self.imap:
            return {"success": False, "error": "Not connected"}
        
        try:
            self.imap.select("INBOX")
            
            for email_id in email_ids:
                self.imap.store(email_id, '+X-GM-LABELS', '\\All')
                self.imap.store(email_id, '+FLAGS', '\\Deleted')
            
            self.imap.expunge()
            
            return {"success": True, "archived": len(email_ids)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def disconnect(self):
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass