from typing import List, Dict, Any
import json
from llm import init_llm

class EmailClusterer:
    def __init__(self):
        self.llm = init_llm()
    
    def cluster_emails(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not emails:
            return []
        
        email_summaries = []
        for email in emails[:200]:
            summary = f"From: {email['from'][:50]}, Subject: {email['subject'][:100]}, Preview: {email['body'][:150]}"
            email_summaries.append(summary)
        
        prompt = f"""Analyze these {len(email_summaries)} emails and group them into 3-5 actionable clusters. 
        For each cluster, provide:
        1. A clear, actionable name (e.g., "Newsletters to Unsubscribe", "Meeting Requests to Schedule", "Bills to Pay")
        2. A brief description of what action to take
        3. The email indices that belong to this cluster (0-indexed)
        
        Return as JSON with this exact structure:
        {{
            "clusters": [
                {{
                    "name": "cluster name",
                    "description": "what to do with these emails",
                    "action": "Archive", 
                    "email_indices": [0, 1, 2],
                    "count": 3,
                    "priority": "high|medium|low"
                }}
            ]
        }}
        
        Email summaries:
        {chr(10).join([f'{i}. {s}' for i, s in enumerate(email_summaries[:100])])}
        
        {f'... and {len(email_summaries) - 100} more emails' if len(email_summaries) > 100 else ''}
        
        Focus on actionability and usefulness. Group by what action the user should take."""
        
        try:
            response = self.llm.invoke(prompt)
            
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            clusters_data = json.loads(content)
            clusters = clusters_data.get("clusters", [])
            
            for cluster in clusters:
                cluster_emails = []
                for idx in cluster.get("email_indices", []):
                    if 0 <= idx < len(emails):
                        cluster_emails.append(emails[idx])
                cluster["emails"] = cluster_emails
                cluster["count"] = len(cluster_emails)
            
            return clusters
        except Exception as e:
            print(f"Error clustering: {e}")
            return self._fallback_clustering(emails)
    
    def _fallback_clustering(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        clusters = []
        
        newsletters = []
        notifications = []
        personal = []
        other = []
        
        for email in emails:
            sender = email.get("from", "").lower()
            subject = email.get("subject", "").lower()
            
            if any(word in sender or word in subject for word in ["newsletter", "digest", "update", "weekly", "daily", "unsubscribe"]):
                newsletters.append(email)
            elif any(word in sender for word in ["notification", "alert", "noreply", "no-reply", "automated"]):
                notifications.append(email)
            elif "@gmail.com" in sender or "@yahoo.com" in sender or "@outlook.com" in sender:
                personal.append(email)
            else:
                other.append(email)
        
        if newsletters:
            clusters.append({
                "name": "Newsletters & Updates",
                "description": "Marketing emails and newsletters - consider unsubscribing from unwanted ones",
                "action": "Archive",
                "emails": newsletters,
                "count": len(newsletters),
                "priority": "low"
            })
        
        if notifications:
            clusters.append({
                "name": "Automated Notifications",
                "description": "System notifications and automated messages",
                "action": "Archive",
                "emails": notifications,
                "count": len(notifications),
                "priority": "low"
            })
        
        if personal:
            clusters.append({
                "name": "Personal Emails",
                "description": "Emails from individuals - review for important messages",
                "action": "Review",
                "emails": personal,
                "count": len(personal),
                "priority": "high"
            })
        
        if other:
            clusters.append({
                "name": "Other Emails",
                "description": "Miscellaneous emails to review",
                "action": "Review",
                "emails": other,
                "count": len(other),
                "priority": "medium"
            })
        
        return clusters