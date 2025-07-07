# Enhanced SEO-Optimized Crypto Article Generator

A powerful Python script that fetches the latest crypto news from Cointelegraph, performs advanced keyword research, and generates SEO-optimized articles with real social media integration and internal backlinks.

## 🚀 Features

### Core Functionality
- **RSS Feed Integration**: Fetches latest articles from Cointelegraph RSS
- **Advanced Keyword Research**: Uses Google Trends and competitor analysis
- **AI-Powered Content Generation**: Creates SEO-optimized articles with low AI detection scores
- **Multiple Content Passes**: Enhances content with human-like writing patterns

### Real API Integrations
- **Twitter/X API**: Fetches real tweets related to crypto topics
- **Tokenfeed.io Scraping**: Finds real internal articles for backlinking
- **Fallback Systems**: Graceful degradation when APIs are unavailable

### SEO Optimization
- **Meta Tags**: Complete SEO meta tag generation
- **Structured Data**: Schema.org markup for better search visibility
- **Keyword Density**: Optimized keyword distribution
- **Reading Time**: Calculated reading time for better UX

### Social Media Integration
- **Real Tweets**: Live Twitter/X integration with engagement metrics
- **Image Prompts**: AI-generated image suggestions for visual content
- **Social Embeds**: Beautiful tweet and image embeds in articles

### Internal Backlinking
- **Real Scraping**: Web scraping of tokenfeed.io for relevant articles
- **Smart Integration**: Natural internal link placement
- **Related Articles**: Automated related articles section

## 📋 Requirements

```bash
pip install -r requirements.txt
```

### Dependencies
- `feedparser` - RSS feed parsing
- `pytrends` - Google Trends integration
- `openai` - AI content generation
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `tweepy` - Twitter/X API integration
- `selenium` - Web scraping for tokenfeed.io
- `webdriver-manager` - Chrome driver management

## ⚙️ Configuration

### Twitter/X API Setup
1. Get API credentials from [Twitter Developer Portal](https://developer.twitter.com/)
2. Update the configuration in `cointelegraph.py`:

```python
TWITTER_BEARER_TOKEN = "your_bearer_token"
TWITTER_API_KEY = "your_api_key"
TWITTER_API_SECRET = "your_api_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_TOKEN_SECRET = "your_access_token_secret"
```

### DeepSeek API
The script uses DeepSeek AI for content generation. Update the API key:

```python
DEEPSEEK_KEY = "your_deepseek_api_key"
```

## 🎯 Usage

### Basic Usage
```bash
python3 cointelegraph.py
```

### What Happens
1. **Fetches Latest Article**: Gets the most recent article from Cointelegraph RSS
2. **Keyword Research**: Analyzes trending crypto keywords and competitor content
3. **Real Social Media**: Searches for relevant tweets using Twitter/X API
4. **Internal Backlinks**: Scrapes tokenfeed.io for related articles
5. **Content Generation**: Creates SEO-optimized article with AI
6. **HTML Export**: Generates fully formatted HTML with all integrations

### Output
- **HTML Files**: SEO-optimized articles saved in `exports/` directory
- **Real Tweets**: Live tweets embedded in articles
- **Internal Links**: Real backlinks from tokenfeed.io
- **Image Prompts**: AI-generated image suggestions

## 🔧 Advanced Features

### AI Detection Avoidance
- **Human Patterns**: Natural transitions and qualifiers
- **Varied Structure**: Mixed sentence lengths and styles
- **Personal Insights**: Expert opinions and conversational elements
- **Multiple Passes**: Content enhancement through multiple AI iterations

### SEO Optimization
- **Meta Tags**: Title, description, keywords, Open Graph, Twitter Cards
- **Structured Data**: Schema.org Article markup
- **Keyword Density**: Optimal 2.5% keyword distribution
- **Reading Time**: Calculated for better user engagement

### Social Media Integration
- **Real Tweets**: Live Twitter/X API integration
- **Engagement Metrics**: Like and retweet counts
- **Author Information**: Real usernames and timestamps
- **Fallback System**: Simulated tweets when API unavailable

### Internal Backlinking
- **Real Scraping**: Selenium-based tokenfeed.io scraping
- **Smart Selection**: Relevance-based article selection
- **Natural Integration**: Contextual link placement
- **Related Sections**: Automated related articles display

## 📊 Performance

### Current Results
- **Word Count**: ~1000-1800 words per article
- **SEO Score**: Optimized for search engines
- **AI Detection**: Low detection scores through human patterns
- **Social Integration**: Real tweets and engagement metrics
- **Internal Links**: Real backlinks from tokenfeed.io

### Fallback Systems
- **Twitter API**: Falls back to simulated tweets if API unavailable
- **Tokenfeed Scraping**: Falls back to generated internal links if scraping fails
- **Content Generation**: Multiple AI passes ensure quality output

## 🛠️ Customization

### Configuration Options
```python
# SEO Settings
TARGET_WORD_COUNT = 1800
KEYWORD_DENSITY = 2.5
MIN_READING_TIME = 7

# Social Media
ENABLE_SOCIAL_MEDIA = True
MAX_TWEETS_PER_ARTICLE = 2

# Internal Links
ENABLE_INTERNAL_LINKS = True
MAX_INTERNAL_LINKS = 3
```

### Adding New Sources
1. **New RSS Feeds**: Update `RSS_URL` variable
2. **Different APIs**: Modify API client initialization
3. **Custom Scraping**: Update Selenium selectors for new sites

## 🔍 Troubleshooting

### Common Issues
1. **Twitter API Errors**: Check credentials and rate limits
2. **Scraping Failures**: Verify tokenfeed.io structure hasn't changed
3. **AI Generation**: Ensure DeepSeek API key is valid
4. **Chrome Driver**: WebDriver Manager handles automatic updates

### Debug Mode
Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Future Enhancements

### Planned Features
- **More Social Platforms**: Reddit, Discord integration
- **Image Generation**: DALL-E/Midjourney integration
- **Analytics**: Article performance tracking
- **Scheduling**: Automated publishing system
- **Multi-language**: Support for different languages

### API Expansions
- **More Crypto Sources**: Additional RSS feeds
- **Enhanced Scraping**: More internal link sources
- **Social Analytics**: Engagement prediction
- **SEO Tools**: Integration with SEMrush/Ahrefs

## 📄 License

This project is for educational and research purposes. Please respect the terms of service of all integrated APIs and websites.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

**Note**: This tool is designed for content creation and SEO optimization. Always ensure compliance with platform terms of service and respect rate limits for all APIs. 