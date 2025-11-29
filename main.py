import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from bs4 import BeautifulSoup

SENDER_EMAIL = "romszikey@gmail.com"
SENDER_PASSWORD = "vale ejlu aaet rtas"
RECEIVER_EMAIL = "romszikey@gmail.com"
CITY = "Ifo"


def get_weather():
    try:
        url = f"https://wttr.in/{CITY}?format=j1"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            description = current['weatherDesc'][0]['value']
            humidity = current['humidity']

            weather_info = f"🌤️ Weather in {CITY}:\n"
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

def send_email(subject, body):
    try:
        message = MIMEMultipart()

        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def create_daily_report():
    print("📊 Generating daily report...\n")

    current_date = datetime.now().strftime("%B %d, %Y")
    current_time = datetime.now().strftime("%I:%M %p")

    report = f"Daily Report for {current_date}\n"
    report += f"Generated at {current_time}\n\n"
    report += "=" * 50 + "\n"

    print("Fetching weather....")
    report += get_weather()
    report += "\n"

    print("Fetching quote....")
    report += get_quote()
    report += "\n"

    print("Fetching news....")
    report += get_news()
    report += "\n"

    print("Fetching GitHub trending....")
    report += get_github_trending()
    report += "\n"

    print("Fetching fun fact....")
    report += get_fun_fact()
    report += "\n"

    report += "=" * 50 + "\n"
    report += "Have a great day! 🚀\n"

    subject = f"Your Daily Report - {current_date}"

    print("\n📧 Sending email...")
    send_email(subject, report)

if __name__ == "__main__":
    print("🚀 Starting Daily Email Reporter\n")
    create_daily_report()
    print("\n✅ All done!")