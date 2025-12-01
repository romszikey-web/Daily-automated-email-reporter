import smtplib
import requests
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')



def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            description = current['weatherDesc'][0]['value']
            humidity = current['humidity']

            weather_info = f"🌤️ Weather in {city}:\n"
            weather_info += f"   Temperature: {temp}°C\n"
            weather_info += f"   Conditions: {description}\n"
            weather_info += f"   Humidity: {humidity}%\n"     

            return weather_info
        else:
            return "❌ Unable to fetch weather data\n"
    except Exception as e:
        return f"❌ Weather error: {str(e)}\n"

def get_quote():
    try:
        url = "https://api.quotable.io/random"
        response = requests.get(url, timeout=30, verify=False)

        if response.status_code == 200:
            data = response.json()
            quote_text = data['content']
            author = data['author']

            quote_info = f"💭 Quote of the Day:\n"
            quote_info += f'   "{quote_text}"\n'
            quote_info += f"   - {author}\n"

            return quote_info
        else:
            return "❌ Unable to fetch quote data\n"
    except Exception as e:
        return f"❌ Quote error: {str(e)}\n"

def get_news():
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            story_ids = response.json()
            news_info = "📰 Top Tech News:\n"
            for i, story_id in enumerate(story_ids[:5],1):
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=15)

                if story_response.status_code == 200:
                    story = story_response.json()
                    title = story.get('title', 'No title')
                    link = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    news_info += f"{i}. {title}\n"
                    news_info += f"   {link}\n\n"
            
            return news_info
        else:
            return "❌ Unable to fetch news\n"

    except Exception as e:
        return f"❌ News error: {str(e)}\n"

def get_github_trending():
    try:
        url = "https://github.com/trending"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ) Applewebkit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            github_info = "⭐ GitHub Trending Repositories:\n"
            repos = soup.find_all('article', class_='Box-row')

            for i, repo in enumerate(repos[:5], 1):
                h2_tag = repo.find('h2')
                if h2_tag:
                    link_tag = h2_tag.find('a')
                    if link_tag:
                        repo_path = link_tag.get('href')
                        repo_name = link_tag.text.strip()
                        repo_name = ' '.join(repo_name.split())
                        repo_url = f"https://github.com{repo_path}"
                        desc_tag = repo.find('p', class_='col-9')
                        description = desc_tag.text.strip() if desc_tag else "No description"

                        github_info += f"{i}. {repo_name}\n"
                        github_info += f"   {repo_url}\n"
                        github_info += f"   {description}\n\n"

            return github_info
        else:
            return "❌ Unable to fetch GitHub trending data\n"
    except Exception as e:
        return f"❌ GitHub trending error: {str(e)}\n"

def get_fun_fact():
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            fact = data['text']

            fact_info = f"🎲 Fun Fact:\n"
            fact_info += f"   {fact}\n"

            return fact_info
        else:
            return "❌ Unable to fetch fun fact\n"
    except Exception as e:
        return f"❌ Fun fact error: {str(e)}\n"

def read_recipients():
    try:
        print("📊 Fetching recipients from Google Sheets...")
        csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
        response = requests.get(csv_url, timeout=30)

        if response.status_code == 200:
            csv_data = response.text.strip().split('\n')

            import io 
            reader = csv.DictReader(io.StringIO(response.text))

            recipients = []
            for row in reader:
                recipients.append({
                    'email': row['email'].strip(),
                    'name': row['name'].strip(),
                    'city': row['city'].strip()
                })

            print(f"✅ Loaded {len(recipients)} recipients from Google Sheets\n")
            return recipients
        else:
            print(f"⚠️ Could not fetch from Google Sheets (Status: {response.status_code})")
            
    except Exception as e:
        print(f"⚠️ Error reading from Google Sheets: {str(e)}")

            
def send_email(recipient_email, recipient_name, subject, body):
    try:
        message = MIMEMultipart()

        message['From'] = SENDER_EMAIL
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print(f"   ✅ Sent to {recipient_name} ({recipient_email})")
        return True

    except Exception as e:
         print(f"   ❌ Failed to send to {recipient_name}: {str(e)}")
    return False

def create_personalized_report(recipient_name, recipient_city, shared_data):
    print("📊 Generating daily report...\n")

    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")

    report = f"Hello {recipient_name}! 👋\n\n"
    report = f"Daily Report for {current_date}\n"
    report += f"Generated at {current_time}\n\n"
    report += "=" * 50 + "\n"

    print(f"   Fetching weather for {recipient_city}...")
    report += get_weather(recipient_city)
    report += "\n"

    report += shared_data['quote']
    report += "\n"
    report += shared_data['news']
    report += "\n"
    report += shared_data['github']
    report += "\n"
    report += shared_data['fact']
    report += "\n"

    report += "=" * 50 + "\n"
    report += "Have a great day! 🚀\n"

    return report

def create_and_send_reports():
    print("📊 Starting Daily Email Reporter...\n")

    recipients = read_recipients()
    if not recipients:
        print("No recipients to send to. Exiting")
        return

        print("📥 Fetching shared data...\n")
    
    shared_data = {}
    
    print("Fetching quote...")
    shared_data['quote'] = get_quote()
    
    print("Fetching news...")
    shared_data['news'] = get_news()
    
    print("Fetching GitHub trending...")
    shared_data['github'] = get_github_trending()
    
    print("Fetching fun fact...")
    shared_data['fact'] = get_fun_fact()
    
    print("\n📧 Sending personalized emails...\n")

    current_date = datetime.now().strftime("%B %d, %Y")

    sent_count = 0
    failed_count = 0

    for recipient in recipients:
        print(f"Processing {recipient['name']}...")

        report = create_personalized_report(
            recipient['name'],
            recipient['city'],
            shared_data
        )
        
        subject = f"Your Daily Report - {current_date}"

        success = send_email(
            recipient['email'],
            recipient['name'],
            subject,
            report
        )

        
        if success:
            sent_count += 1
        else:
            failed_count += 1

        print()

    print("=" * 50)
    print(f"✅ Successfully sent: {sent_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total recipients: {len(recipients)}")

if __name__ == "__main__":
    print("🚀 Daily Email Reporter - Multi-User Version\n")
    create_and_send_reports()
    print("\n✅ All done!")