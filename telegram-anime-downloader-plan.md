# Telegram Anime Downloader Bot - Project Plan

## 🎯 Project Overview

A Telegram bot that scrapes anime from AnimePahe, downloads episodes, and uploads them to Telegram's cloud storage for easy access on any device (especially Oppo A3s with browser limitations).

### Vision: Telegram as Automation Command Interface
This bot is the **first step** in building a comprehensive automation system where Telegram serves as the command center for various automated tasks.

---

## 📖 How to Use This Document

### When You're Ready to Start Building

Open this document and say to your AI assistant (Claude, ChatGPT, or any other):

```
"I want to build the Telegram Anime Downloader Bot according to the plan in telegram-anime-downloader-plan.md. 

Let's start with Phase 1 only - the basic functionality. I want to build this incrementally, not all at once.

Help me with Step 1: Setup & Configuration first. Guide me through each step and explain what I'm doing."
```

### Important: Incremental Development Approach ⚠️

**DO NOT try to build everything at once!** This is a learning project. Follow this approach:

1. **Start Small** - Build the absolute minimum first (just bot connection + /start and /help commands)
2. **Test Often** - Make sure each piece works before moving to the next
3. **One Feature at a Time** - Don't jump ahead to batch downloads before single download works
4. **Ask Questions** - If something doesn't make sense, ask before continuing
5. **Take Breaks** - This is a multi-day project, not a one-sitting sprint

### Recommended Build Order

```
Session 1 (1-2 hours):
├── Setup bot with @BotFather
├── Get bot working with /start and /help
└── Test connection

Session 2 (2-3 hours):
├── Build basic AnimePahe scraper (search only)
├── Make /search command work
└── Display search results

Session 3 (2-3 hours):
├── Get download link extraction working
├── Download ONE episode manually
└── Save to local file

Session 4 (1-2 hours):
├── Upload that file to Telegram
├── Make it work end-to-end for ONE episode
└── Celebrate! 🎉 You now have a working bot!

Later Sessions (optional):
├── Add quality selection
├── Add batch download
├── Add database
└── Add advanced features
```

### What NOT to Do ❌

- ❌ Don't try to build all features in Phase 1, 2, and 3 at once
- ❌ Don't add database/queue system until basic download works
- ❌ Don't focus on error handling before core features work
- ❌ Don't get overwhelmed - you don't need everything immediately

### What TO Do ✅

- ✅ Build the simplest version first (/start, /help only)
- ✅ Make ONE episode download work before batch
- ✅ Test each piece thoroughly
- ✅ Ask for help when stuck
- ✅ Focus on learning, not speed

### 📝 Code Comments Requirement

**IMPORTANT FOR AI ASSISTANTS:** When providing code, include **detailed comments** explaining what each line does. This is a **learning project**, not production code.

Example of good commenting:

```python
# Import the Telegram bot library
import telebot

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Create bot instance using token from environment variable
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# Define handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Send a welcome message back to the user
    bot.reply_to(message, "Welcome! Use /help for commands.")
```

**Every code snippet should:**
- Explain imports and why they're needed
- Comment each function's purpose
- Explain what each line does (especially for complex logic)
- Include inline comments for non-obvious code
- Help the learner understand, not just copy-paste

---

## 🌟 Why This Approach?

### Problem Being Solved:
- ❌ Oppo A3s has Chrome download issues
- ❌ Can't run Brave browser on device
- ❌ Limited phone storage
- ❌ Need reliable way to download and watch anime

### Solution Benefits:
- ✅ **Unlimited cloud storage** (Telegram allows up to 2GB per file)
- ✅ **Watch directly in Telegram** app (no external player needed)
- ✅ **Access from any device** (PC, phone, tablet)
- ✅ **No phone storage used** (stream from cloud or download when needed)
- ✅ **Simple command interface** (just chat with the bot)
- ✅ **Persistent storage** (videos stay in chat history forever)

---

## 📋 Core Features

### Phase 1: Basic Functionality
- [ ] Search for anime by name
- [ ] List available episodes for a series
- [ ] Download single episode
- [ ] Upload to Telegram chat
- [ ] Quality selection (720p, 1080p)

### Phase 2: Advanced Features
- [ ] Batch download (multiple episodes at once)
- [ ] Real-time progress updates
- [ ] Auto-naming with series name and episode number
- [ ] Resume failed downloads
- [ ] Queue management (handle multiple requests)

### Phase 3: Power User Features
- [ ] Schedule downloads (download at night when internet is faster)
- [ ] Auto-download new episodes (subscribe to ongoing series)
- [ ] Format conversion (MP4 → MKV if needed)
- [ ] Subtitle extraction and embedding
- [ ] Episode tracking (mark watched/unwatched)

---

## 🏗️ Technical Architecture

### Technology Stack

```
┌─────────────────────────────────────────┐
│           User (Telegram App)           │
└─────────────────┬───────────────────────┘
                  │ Commands (/download, /search)
                  ▼
┌─────────────────────────────────────────┐
│         Telegram Bot (pyTelegramBotAPI) │
│         - Receives commands             │
│         - Sends updates/files           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Bot Logic (Python)              │
│         - Command parsing               │
│         - Queue management              │
│         - Progress tracking             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    AnimePahe Scraper (BeautifulSoup)    │
│         - Search anime                  │
│         - Extract episode links         │
│         - Get download URLs             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│      Video Downloader (requests)        │
│         - Download video files          │
│         - Handle progress tracking      │
│         - Resume support               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Optional: FFmpeg (Conversion)        │
│         - Convert formats               │
│         - Embed subtitles              │
│         - Compress if needed           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Telegram Upload (Bot API)            │
│         - Upload to Telegram cloud      │
│         - Send to user chat            │
└─────────────────────────────────────────┘
```

### Required Python Libraries

```python
# Core
import telebot  # pip install pyTelegramBotAPI
import requests  # HTTP requests
from bs4 import BeautifulSoup  # HTML parsing

# Optional
import ffmpeg  # Video conversion
import sqlite3  # Database for tracking
from pathlib import Path  # File handling
import asyncio  # Async operations
from tqdm import tqdm  # Progress bars
```

---

## 🚀 Bot Commands Design

### User-Facing Commands

```
/start - Welcome message and instructions
/help - Show all available commands
/search <anime_name> - Search for anime
/list <anime_id> - List all episodes for a series
/download <episode_url> - Download single episode
/batch <anime_id> <start>-<end> - Download multiple episodes
/queue - Show current download queue
/cancel <download_id> - Cancel a download
/settings - Configure quality, format, etc.
/status - Bot status and statistics
```

### Example Usage Flow

```
User: /start
Bot: 👋 Welcome! I can help you download anime from AnimePahe.
     Use /search to find anime or /help for all commands.

User: /search one piece
Bot: 🔍 Search results:
     1. One Piece (Ongoing)
     2. One Piece Film: Red
     3. One Piece: Stampede
     
     Reply with number or use /list <id>

User: 1
Bot: 📺 One Piece - 1000+ episodes available
     Use /download <episode_number> or /batch <start>-<end>
     
     Latest episodes:
     - Episode 1088
     - Episode 1087
     - Episode 1086

User: /download 1088
Bot: ⬇️ Downloading One Piece Ep 1088...
     Quality: 1080p | Size: ~400MB
     Progress: [████████░░] 80%

Bot: ✅ Download complete!
     📤 Uploading to Telegram...

Bot: [Video uploaded to chat]
     🎬 One Piece - Episode 1088 (1080p)
     ⏱️ Duration: 23:45
```

---

## 💾 Data Storage

### SQLite Database Schema

```sql
-- Track user preferences
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    telegram_username TEXT,
    preferred_quality TEXT DEFAULT '1080p',
    preferred_format TEXT DEFAULT 'mp4',
    notifications_enabled BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track downloads
CREATE TABLE downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    anime_name TEXT,
    episode_number INTEGER,
    quality TEXT,
    status TEXT, -- pending, downloading, uploading, completed, failed
    file_path TEXT,
    telegram_file_id TEXT, -- For re-sending without re-uploading
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Track anime series (cache)
CREATE TABLE anime_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anime_name TEXT,
    animepahe_id TEXT,
    total_episodes INTEGER,
    last_updated TIMESTAMP,
    UNIQUE(animepahe_id)
);
```

---

## 🔧 Implementation Steps

### Step 1: Setup & Configuration (30 min)

1. Create new project directory
2. Set up virtual environment
3. Install dependencies
4. Create Telegram bot via @BotFather
5. Get bot token
6. Create `.env` file for secrets

```bash
mkdir telegram-anime-bot
cd telegram-anime-bot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install pyTelegramBotAPI requests beautifulsoup4 python-dotenv
```

```env
# .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
DOWNLOAD_PATH=./downloads
MAX_FILE_SIZE_MB=2000
```

### Step 2: Basic Bot Structure (1 hour)

```python
# bot.py - Main bot file structure

import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /help for commands.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Available commands:
    /search <name> - Search anime
    /download <url> - Download episode
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['search'])
def search_anime(message):
    # TODO: Implement search
    pass

@bot.message_handler(commands=['download'])
def download_episode(message):
    # TODO: Implement download
    pass

if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling()
```

### Step 3: AnimePahe Scraper (2 hours)

```python
# scraper.py - AnimePahe scraping logic

import requests
from bs4 import BeautifulSoup

class AnimePaheScraper:
    BASE_URL = "https://animepahe.com"
    
    def search(self, query):
        """Search for anime by name"""
        # Implementation:
        # 1. Send GET request to search endpoint
        # 2. Parse HTML response
        # 3. Extract anime titles, IDs, thumbnails
        # 4. Return list of results
        pass
    
    def get_episodes(self, anime_id):
        """Get all episodes for an anime"""
        # Implementation:
        # 1. Fetch anime page
        # 2. Parse episodes list
        # 3. Extract episode numbers and URLs
        # 4. Return list of episodes
        pass
    
    def get_download_link(self, episode_url, quality='1080p'):
        """Extract actual download link for an episode"""
        # Implementation:
        # 1. Navigate to episode page
        # 2. Find download links (may require multiple requests)
        # 3. Select requested quality
        # 4. Return direct download URL
        pass
```

### Step 4: Download Manager (1.5 hours)

```python
# downloader.py - Video download logic

import requests
from pathlib import Path

class VideoDownloader:
    def __init__(self, download_path='./downloads'):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
    
    def download(self, url, filename, progress_callback=None):
        """Download video with progress tracking"""
        # Implementation:
        # 1. Send GET request with stream=True
        # 2. Get total file size from headers
        # 3. Download in chunks
        # 4. Call progress_callback with percentage
        # 5. Save to file
        # 6. Return file path
        pass
    
    def cleanup(self, filepath):
        """Delete downloaded file after upload"""
        if Path(filepath).exists():
            Path(filepath).unlink()
```

### Step 5: Telegram Integration (1 hour)

```python
# telegram_handler.py - Telegram-specific functions

def upload_video(bot, chat_id, filepath, caption, progress_callback=None):
    """Upload video to Telegram"""
    with open(filepath, 'rb') as video:
        bot.send_video(
            chat_id=chat_id,
            video=video,
            caption=caption,
            supports_streaming=True
        )

def send_progress(bot, chat_id, message_id, progress):
    """Update progress message"""
    progress_bar = '█' * int(progress / 10) + '░' * (10 - int(progress / 10))
    text = f"⬇️ Downloading... [{progress_bar}] {progress}%"
    bot.edit_message_text(text, chat_id, message_id)
```

### Step 6: Queue System (Optional, 1 hour)

```python
# queue_manager.py - Handle concurrent downloads

from queue import Queue
from threading import Thread

class DownloadQueue:
    def __init__(self, max_concurrent=2):
        self.queue = Queue()
        self.max_concurrent = max_concurrent
        self.active_downloads = {}
    
    def add(self, download_task):
        """Add download to queue"""
        self.queue.put(download_task)
    
    def process(self):
        """Process queue with max concurrent downloads"""
        # Implementation:
        # 1. Start worker threads
        # 2. Process downloads from queue
        # 3. Limit concurrent downloads
        # 4. Handle errors
        pass
```

---

## 📤 Telegram Cloud Storage Details

### File Size Limits
- **Max file size:** 2GB per file
- **Recommended:** Keep files under 1.5GB for faster uploads
- **Anime episodes:** Typically 150-500MB (1080p)

### Upload/Download on Phone
- **Download to phone:** Tap video → "Save to Gallery" or "Save to Downloads"
- **Stream from cloud:** Just tap to play in Telegram
- **Share:** Forward to other chats or users
- **Access:** Available on all devices logged into your Telegram account

### Storage Management
```
Your Telegram chat = Your anime library
- Videos organized by date sent
- Use chat search to find episodes
- Create separate chat/channel for organization
- Bot can send to specific chat/channel
```

---

## 🎮 Future Automation Ideas (Telegram as Command Center)

Since this is Step 1 of your automation vision, here are ideas for expansion:

### Possible Future Bots/Commands
1. **File Management Bot**
   - `/organize` - Auto-organize downloads
   - `/backup` - Backup files to cloud
   
2. **System Control Bot**
   - `/shutdown` - Shutdown PC remotely
   - `/status` - Check PC status
   - `/screenshot` - Take screenshot
   
3. **Download Manager Bot**
   - `/yt <url>` - Download YouTube videos
   - `/torrent <magnet>` - Add torrent
   
4. **Notification Bot**
   - Get alerts for system events
   - Monitor long-running tasks
   - Daily reports

All controlled through one Telegram interface! 🚀

---

## 🐛 Error Handling & Edge Cases

### Common Issues to Handle

1. **Network Errors**
   - Retry failed downloads (max 3 attempts)
   - Resume interrupted downloads
   - Timeout handling

2. **AnimePahe Changes**
   - Site structure changes (scraping breaks)
   - Cloudflare protection
   - Rate limiting

3. **File Size Issues**
   - Files > 2GB (split or compress)
   - Quality downgrade option
   - Alert user before download

4. **Telegram Limits**
   - API rate limits (20 messages/minute)
   - Upload speed throttling
   - Chat storage limits

### Error Messages

```python
ERROR_MESSAGES = {
    'not_found': '❌ Anime not found. Try different search terms.',
    'too_large': '⚠️ File too large (>2GB). Download lower quality?',
    'network': '🌐 Network error. Retrying...',
    'rate_limit': '⏰ Too many requests. Please wait.',
    'invalid_quality': '❌ Quality not available. Available: 720p, 1080p'
}
```

---

## 🔐 Security & Privacy

### Best Practices

1. **API Keys**
   - Store in `.env` file
   - Never commit to git
   - Use `.gitignore`

2. **User Privacy**
   - Don't log personal data
   - Auto-delete downloaded files after upload
   - Optional: Encrypt database

3. **Bot Access**
   - Make bot private (only you can use)
   - Or implement user whitelist
   - Rate limit per user

```python
# Example: User whitelist
ALLOWED_USERS = [123456789]  # Your Telegram user ID

@bot.message_handler(commands=['download'])
def download(message):
    if message.from_user.id not in ALLOWED_USERS:
        bot.reply_to(message, "❌ Unauthorized")
        return
    # ... rest of code
```

---

## 📁 Project Structure

```
telegram-anime-bot/
├── .env                    # Environment variables (NEVER commit)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── bot.py                # Main bot entry point
├── scraper.py            # AnimePahe scraper
├── downloader.py         # Video downloader
├── telegram_handler.py   # Telegram utilities
├── queue_manager.py      # Download queue (optional)
├── database.py           # SQLite database handler
├── config.py             # Configuration settings
├── downloads/            # Temporary download folder
└── logs/                 # Log files
```

---

## 🚦 Getting Started Checklist

When ready to build, follow this order:

- [ ] Create Telegram bot with @BotFather, get token
- [ ] Set up project structure and virtual environment
- [ ] Install dependencies
- [ ] Implement basic bot (start, help commands)
- [ ] Test bot connection
- [ ] Build AnimePahe scraper (search function)
- [ ] Build AnimePahe scraper (episode list function)
- [ ] Build AnimePahe scraper (download link extraction)
- [ ] Implement video downloader with progress
- [ ] Integrate downloader with bot
- [ ] Test single episode download + upload
- [ ] Add quality selection
- [ ] Add batch download feature
- [ ] Implement queue system (optional)
- [ ] Add database tracking (optional)
- [ ] Add error handling
- [ ] Test on Oppo A3s phone
- [ ] Add advanced features

---

## 🎓 Learning Resources

### Telegram Bot Development
- [pyTelegramBotAPI Documentation](https://github.com/eternnoir/pyTelegramBotAPI)
- [Telegram Bot API](https://core.telegram.org/bots/api)

### Web Scraping
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)

### Video Processing
- [FFmpeg Python](https://github.com/kkroening/ffmpeg-python)

---

## 📝 Notes for Future AI/Conversations

### Context for Implementation
- **User device:** Oppo A3s with browser limitations
- **Primary use:** Personal anime viewing
- **Learning focus:** Web scraping, Telegram bots, automation
- **Future vision:** Telegram as central automation interface
- **Personal use:** Ethical usage for learning and convenience

### Key Design Decisions
1. Use Telegram cloud to bypass phone storage/browser issues
2. Start simple, add features incrementally
3. Focus on reliability over features initially
4. Keep user experience simple (chat commands)
5. Make it extensible for future automation projects

### Technical Constraints
- Max 2GB per file on Telegram
- AnimePahe structure may change (scraping fragility)
- Need to handle Cloudflare protection
- Rate limiting considerations

---

## ✅ Success Criteria

This project is successful when:
- ✅ Can search for anime by name
- ✅ Can download single episode
- ✅ Video uploaded to Telegram cloud
- ✅ Can watch on Oppo A3s from Telegram app
- ✅ Code is clean and documented
- ✅ Error handling works reliably
- ✅ Learning objectives met (scraping, bots, automation)

---

**Project Status:** 📋 Planning Complete - Ready for Implementation

**Estimated Time:** 6-8 hours for basic version, 12-16 hours for full-featured

**Next Steps:** When ready, create new workspace and start with Step 1 (Setup & Configuration)
