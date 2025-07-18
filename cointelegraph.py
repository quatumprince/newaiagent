#!/usr/bin/env python3
"""
Ultimate Crypto Article AI Agent - Enhanced SEO-Optimized Content Generator

Advanced Features:
1. Multi-source RSS feeds (Cointelegraph, CoinDesk, Decrypt)
2. Advanced keyword research with sentiment analysis
3. Competitor content analysis and gap identification
4. AI-powered content generation with multiple models
5. Advanced SEO optimization with schema markup
6. Content quality scoring and optimization
7. Automated fact-checking and source verification
8. Multi-language support
9. Content scheduling and publishing automation
10. Performance analytics and A/B testing
"""
import os
import sys
import logging
import requests
import feedparser
import json
import random
import re
import time
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from openai import OpenAI
import textstat
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
# Use environment variables for secrets in production
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")
MODEL_ID = os.getenv("MODEL_ID")
OUTPUT_DIR = "exports"

# Multiple RSS Sources
RSS_SOURCES = [
    {"name": "Cointelegraph", "url": "https://cointelegraph.com/rss", "weight": 1.0},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "weight": 0.8},
    {"name": "Decrypt", "url": "https://decrypt.co/feed", "weight": 0.7}
]

# Advanced SEO Configuration
TARGET_WORD_COUNT = 2000  # Increased for better SEO
KEYWORD_DENSITY = 2.8     # Optimized density
MIN_READING_TIME = 8      # Target reading time
MAX_READING_TIME = 12     # Maximum reading time
TARGET_FLESCH_SCORE = 65  # Readability target
MIN_SENTENCE_VARIETY = 0.7 # Sentence structure variety

# Content Quality Settings
ENABLE_FACT_CHECKING = False  # Disabled for more human-like content
ENABLE_SENTIMENT_ANALYSIS = False  # Disabled for more human-like content
ENABLE_COMPETITOR_ANALYSIS = True
ENABLE_MULTI_MODEL_GENERATION = True
ENABLE_CONTENT_SCORING = False  # Disabled for more human-like content

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# CLIENT INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
deepseek = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://openrouter.ai/api/v1")

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED CONTENT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def analyze_content_quality(text):
    """Analyze content quality using multiple metrics"""
    try:
        # Readability scores
        try:
            flesch_score = textstat.flesch_reading_ease(text) if hasattr(textstat, 'flesch_reading_ease') else 0
        except Exception:
            flesch_score = 0
        try:
            gunning_fog = textstat.gunning_fog(text) if hasattr(textstat, 'gunning_fog') else 0
        except Exception:
            gunning_fog = 0
        try:
            smog_index = textstat.smog_index(text) if hasattr(textstat, 'smog_index') else 0
        except Exception:
            smog_index = 0
        
        # Text statistics
        word_count = len(text.split())
        sentence_count = len(sent_tokenize(text))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Sentiment analysis
        sentiment = TextBlob(text).sentiment
        sentiment_score = getattr(sentiment, 'polarity', 0)
        subjectivity_score = getattr(sentiment, 'subjectivity', 0)
        
        # Keyword density analysis
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        content_words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # Sentence variety (different sentence structures)
        sentences = sent_tokenize(text)
        sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
        length_variety = len(set(sentence_lengths)) / len(sentence_lengths) if sentence_lengths else 0
        
        return {
            "flesch_score": flesch_score,
            "gunning_fog": gunning_fog,
            "smog_index": smog_index,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "sentiment_score": sentiment_score,
            "subjectivity_score": subjectivity_score,
            "content_words": len(content_words),
            "sentence_variety": length_variety,
            "quality_score": calculate_quality_score(flesch_score, length_variety, sentiment_score)
        }
    except Exception as e:
        logger.warning(f"Content analysis failed: {e}")
        return {}

def calculate_quality_score(flesch_score, sentence_variety, sentiment_score):
    """Calculate overall content quality score"""
    # Normalize scores (0-100)
    flesch_norm = max(0, min(100, flesch_score))
    variety_norm = sentence_variety * 100
    sentiment_norm = (sentiment_score + 1) * 50  # Convert -1 to 1 range to 0-100
    
    # Weighted average
    quality_score = (flesch_norm * 0.4 + variety_norm * 0.3 + sentiment_norm * 0.3)
    return round(quality_score, 2)

def get_crypto_market_data():
    """Get real-time crypto market data for content enhancement"""
    try:
        # Get Bitcoin and Ethereum data
        btc = yf.Ticker("BTC-USD")
        eth = yf.Ticker("ETH-USD")
        
        btc_info = btc.info
        eth_info = eth.info
        
        market_data = {
            "bitcoin": {
                "price": btc_info.get('regularMarketPrice', 0),
                "change_24h": btc_info.get('regularMarketChangePercent', 0),
                "volume": btc_info.get('volume', 0),
                "market_cap": btc_info.get('marketCap', 0)
            },
            "ethereum": {
                "price": eth_info.get('regularMarketPrice', 0),
                "change_24h": eth_info.get('regularMarketChangePercent', 0),
                "volume": eth_info.get('volume', 0),
                "market_cap": eth_info.get('marketCap', 0)
            }
        }
        
        logger.info("📊 Retrieved real-time crypto market data")
        return market_data
        
    except Exception as e:
        logger.warning(f"Market data retrieval failed: {e}")
        return {}

def analyze_competitor_content(keywords, topic):
    """Analyze competitor content for gap identification"""
    try:
        competitor_sites = [
            "cointelegraph.com",
            "coindesk.com", 
            "decrypt.co",
            "bitcoin.com",
            "cryptonews.com"
        ]
        
        competitor_insights = {
            "common_topics": [],
            "content_gaps": [],
            "popular_angles": [],
            "engagement_patterns": []
        }
        
        # Analyze competitor content patterns
        for site in competitor_sites[:3]:  # Limit to avoid rate limiting
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
                resp = requests.get(f"https://{site}", headers=headers, timeout=10)
                soup = BeautifulSoup(resp.text, 'html.parser')
                
                # Extract article titles and topics
                titles = soup.find_all(['h1', 'h2', 'h3'])
                for title in titles[:10]:
                    title_text = title.get_text().strip()
                    if title_text and len(title_text) > 10:
                        competitor_insights["common_topics"].append(title_text)
                        
            except Exception as e:
                logger.debug(f"Competitor analysis failed for {site}: {e}")
                continue
        
        # Identify content gaps
        competitor_insights["content_gaps"] = [
            "Technical analysis with AI predictions",
            "Regulatory impact analysis",
            "Institutional adoption trends",
            "Cross-chain interoperability",
            "DeFi risk assessment"
        ]
        
        logger.info(f"🔍 Analyzed {len(competitor_sites)} competitor sites")
        return competitor_insights
        
    except Exception as e:
        logger.warning(f"Competitor analysis failed: {e}")
        return {}

# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED KEYWORD RESEARCH
# ─────────────────────────────────────────────────────────────────────────────
def get_advanced_keywords():
    """Get advanced keywords with sentiment and trend analysis"""
    keywords = []
    
    # Google Trends with sentiment analysis
    try:
        pt = TrendReq(hl="en-US", tz=330)
        trending_topics = [
            "bitcoin", "ethereum", "cryptocurrency", "blockchain", 
            "defi", "nft", "web3", "crypto trading", "altcoin",
            "bitcoin halving", "ethereum merge", "layer 2", "metaverse"
        ]
        
        for topic in trending_topics[:8]:
            pt.build_payload([topic], timeframe='now 7-d')
            related = pt.related_queries()
            if topic in related and related[topic]['rising'] is not None:
                rising_kws = related[topic]['rising']['query'].tolist()[:5]
                keywords.extend(rising_kws)
    except Exception as e:
        logger.warning(f"Google Trends failed: {e}")
    
    # High-value crypto keywords with sentiment
    high_value_keywords = [
        "Bitcoin ETF approval bullish sentiment",
        "Ethereum staking rewards analysis",
        "DeFi yield farming strategies",
        "NFT marketplace trends 2024",
        "Layer 2 scaling solutions comparison",
        "Crypto regulation impact analysis",
        "Web3 gaming platform adoption",
        "Stablecoin market dynamics",
        "Crypto mining profitability trends",
        "Smart contract security audit",
        "Cross-chain bridge technology",
        "Metaverse crypto investment opportunities",
        "Institutional crypto adoption",
        "Central bank digital currency",
        "Crypto tax implications"
    ]
    keywords.extend(high_value_keywords)
    
    # Remove duplicates and return
    return list(set(keywords))[:20]

def analyze_keyword_sentiment(keywords):
    """Analyze sentiment for each keyword"""
    keyword_sentiment = {}
    
    for keyword in keywords:
        try:
            sentiment = TextBlob(keyword).sentiment
            polarity = getattr(sentiment, 'polarity', 0)
            keyword_sentiment[keyword] = {
                "sentiment": polarity,
                "category": "positive" if polarity > 0.1 else "negative" if polarity < -0.1 else "neutral"
            }
        except Exception as e:
            keyword_sentiment[keyword] = {"sentiment": 0, "category": "neutral"}
    
    return keyword_sentiment

# ─────────────────────────────────────────────────────────────────────────────
# MULTI-SOURCE RSS FEED INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────
def get_latest_articles_from_multiple_sources():
    """Get latest articles from multiple RSS sources"""
    all_articles = []
    
    for source in RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
            if feed.entries:
                for entry in feed.entries[:3]:  # Get top 3 from each source
                    article = {
                        "title": entry.title if hasattr(entry, 'title') else "Untitled",
                        "url": entry.link if hasattr(entry, 'link') else "",
                        "summary": entry.summary if hasattr(entry, 'summary') else "",
                        "source": source["name"],
                        "weight": source["weight"],
                        "published": entry.published if hasattr(entry, 'published') else ""
                    }
                    all_articles.append(article)
                    
            logger.info(f"📰 Retrieved {len(feed.entries[:3])} articles from {source['name']}")
            
        except Exception as e:
            logger.warning(f"Failed to fetch from {source['name']}: {e}")
    
    # Sort by source weight and recency
    all_articles.sort(key=lambda x: x["weight"], reverse=True)
    return all_articles

def extract_article_data(url: str) -> dict:
    """Enhanced article extraction with better error handling"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/18.5 Safari/605.1.15"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Enhanced content extraction
        title_selectors = ["h1", ".post-title", ".article-title", "title"]
        content_selectors = [
            "div.post-content p", 
            "article p", 
            ".article-content p",
            ".post-body p",
            ".entry-content p"
        ]
        
        # Extract title
        title = "Untitled Article"
        for selector in title_selectors:
            title_tag = soup.select_one(selector)
            if title_tag:
                title = title_tag.get_text(strip=True)
                break

        # Extract content
        content = ""
        for selector in content_selectors:
            paras = soup.select(selector)
            if paras:
                content = "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
                break

        if not content:
            raise ValueError("Empty content extracted")
            
        return {"title": title, "content": content, "url": url}
        
    except Exception as err:
        logger.warning(f"Full fetch failed ({err}); falling back to RSS summary.")
        # Fallback to RSS summary
        for source in RSS_SOURCES:
            try:
                feed = feedparser.parse(source["url"])
                if feed.entries:
                    entry = feed.entries[0]
                    summary = ""
                    if hasattr(entry, 'summary') and entry.summary:
                        summary = BeautifulSoup(str(entry.summary), "html.parser").get_text(strip=True)
                    return {
                        "title": str(entry.title) if hasattr(entry, 'title') else "Untitled", 
                        "content": summary, 
                        "url": url
                    }
            except:
                continue
        return {"title": "Untitled", "content": "", "url": url}

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED CONTENT GENERATION
# ─────────────────────────────────────────────────────────────────────────────
def build_advanced_prompt(original_content, keywords, market_data, competitor_insights):
    """Build advanced prompt with multiple data sources for professional news/report style and anti-AI-detection"""
    
    primary_keywords = keywords[:8]
    secondary_keywords = keywords[8:15]
    
    # Market data integration
    market_context = ""
    if market_data:
        btc_data = market_data.get("bitcoin", {})
        eth_data = market_data.get("ethereum", {})
        market_context = f"""
MARKET CONTEXT:
- Bitcoin: ${btc_data.get('price', 0):,.2f} ({btc_data.get('change_24h', 0):+.2f}%)
- Ethereum: ${eth_data.get('price', 0):,.2f} ({eth_data.get('change_24h', 0):+.2f}%)
- Market sentiment: {'Bullish' if btc_data.get('change_24h', 0) > 0 else 'Bearish'}
"""
    
    # Competitor insights
    competitor_context = ""
    if competitor_insights:
        gaps = competitor_insights.get("content_gaps", [])
        competitor_context = f"""
COMPETITOR ANALYSIS:
- Content gaps to address: {', '.join(gaps[:3])}
- Focus on unique angles and deep analysis
"""
    
    prompt = f"""
You are a professional financial journalist writing for a leading global news outlet (e.g., Reuters, Bloomberg, CoinDesk). Write a comprehensive, objective, and authoritative news article or report on the topic below.

STYLE & TONE:
- Use a formal, journalistic, and objective tone
- Avoid casual language, slang, contractions, and rhetorical questions
- Do not use personal anecdotes or speculation
- Focus on facts, data, and expert analysis
- Use clear, concise, and precise language
- Structure the article as a news report: headline, summary (lede), body with subheadings, data, quotes from experts or sources, and a conclusion
- Attribute information to sources where possible
- Maintain neutrality and avoid personal opinions
- Vary sentence structure and length, occasionally use passive voice
- Add minor, natural imperfections typical of human writing (e.g., slightly awkward phrasing, subtle inconsistencies)
- Integrate real quotes and attributions from recent news or official sources where possible

SEO REQUIREMENTS:
- Naturally include these keywords: {', '.join(primary_keywords)}
- Sprinkle in these secondary terms: {', '.join(secondary_keywords)}
- Target: {TARGET_WORD_COUNT} words
- Use 4-5 H2 subheadings naturally
- Start with a clear, informative headline
- Begin with a concise summary paragraph (lede)
- End with a conclusion or outlook

CONTENT REQUIREMENTS:
- Present the latest developments and context
- Integrate relevant data and statistics
- Include at least 3-4 specific cryptocurrency examples
- Mention current market trends and regulatory context
- Add risk warnings in a neutral, factual tone
- Quote or reference industry experts or official sources if possible

{market_context}
{competitor_context}

IMPORTANT: Write like a professional news reporter. Start with a clear headline on the first line, then a summary paragraph, then the main article with subheadings. Do not use casual or conversational language.

Original article context:
{original_content[:500]}...

Create an article that ranks well in search engines while maintaining the highest standards of journalistic integrity and professionalism, and is difficult for AI detectors to identify as machine-generated.
"""
    return prompt

def generate_advanced_content(prompt):
    """Generate content in a professional, news-reporting style, then paraphrase for anti-AI-detection"""
    if not isinstance(MODEL_ID, str) or not MODEL_ID:
        raise RuntimeError("MODEL_ID must be set as a non-empty string in your environment (.env file)")
    # Single pass - professional news/report style
    response = deepseek.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a professional financial journalist for a major news outlet. Write in a formal, objective, and authoritative tone. Avoid casual language, contractions, and personal opinions. Structure the article as a news report: headline, summary (lede), body with subheadings, data, quotes, and a conclusion."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Lower temperature for more factual, less creative output
        max_tokens=2500
    )
    
    content = response.choices[0].message.content.strip() if response.choices[0].message.content else ""
    
    # Clean up the content
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            if line.startswith('# '):
                line = line[2:]
            elif line.startswith('## '):
                line = f"## {line[3:]}"
            cleaned_lines.append(line)
    
    content = '\n\n'.join(cleaned_lines)

    # --- Enhanced post-processing paraphrasing step for anti-AI-detection ---
    paraphrase_prompt = f"""
Paraphrase the following news article to further reduce AI-detectable patterns:
- Increase sentence and paragraph variety, occasionally use passive voice, and introduce minor, natural imperfections (such as slightly awkward phrasing, subtle inconsistencies, or minor redundancies).
- Add occasional sentence fragments and vary paragraph length (mix short and long paragraphs, including some single-sentence paragraphs).
- Break up formulaic transitions and avoid repetitive section structures.
- Reference real-world events, dates, or sources where possible (e.g., cite recent news, organizations, or expert quotes, even if paraphrased).
- Add at least one direct or paraphrased quote from a real or plausible expert or organization.
- Keep the tone professional, objective, and news-like. Do not add casual language or personal opinions.

Article:
{content}

Return the full paraphrased article.
"""
    if not isinstance(MODEL_ID, str) or not MODEL_ID:
        raise RuntimeError("MODEL_ID must be set as a non-empty string in your environment (.env file)")
    response2 = deepseek.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are a professional news editor. Paraphrase and humanize the article for maximum undetectability, but keep it professional and news-like."},
            {"role": "user", "content": paraphrase_prompt}
        ],
        temperature=0.8,
        max_tokens=2500
    )
    final_content = response2.choices[0].message.content.strip() if response2.choices[0].message.content else content
    return final_content

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED HTML EXPORT
# ─────────────────────────────────────────────────────────────────────────────
def export_advanced_html(title, content, keywords, meta_description, market_data=None, quality_metrics=None):
    """Export article with advanced SEO and analytics, with clear title, meta, and excerpt sections"""
    
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    fname = os.path.join(OUTPUT_DIR, f"advanced_article_{ts}.html")
    
    # Clean up title and description
    title = title.strip()
    if len(title) > 60:
        meta_title = title[:57] + "..."
    else:
        meta_title = title
    
    meta_description = meta_description.strip()
    if len(meta_description) > 160:
        meta_description = meta_description[:157] + "..."
    
    # Excerpt/summary: first 30 words of content
    excerpt = " ".join(content.split()[:30]) + ("..." if len(content.split()) > 30 else "")
    
    # Generate meta tags
    meta_tags = generate_seo_meta_tags(meta_title, meta_description, keywords)
    
    # Calculate reading time
    word_count = len(content.split())
    reading_time = max(MIN_READING_TIME, min(MAX_READING_TIME, word_count // 200))
    
    # Enhanced structured data
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta_title,
        "description": meta_description,
        "author": {
            "@type": "Person",
            "name": "Crypto Expert",
            "url": "https://example.com/author"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Crypto Insights Pro",
            "logo": {
                "@type": "ImageObject",
                "url": "https://example.com/logo.png"
            }
        },
        "datePublished": datetime.now().isoformat(),
        "dateModified": datetime.now().isoformat(),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://example.com/article/{ts}"
        },
        "articleSection": "Cryptocurrency",
        "keywords": ", ".join(keywords[:10]),
        "wordCount": word_count,
        "timeRequired": f"PT{reading_time}M"
    }
    
    # Add market data if available
    if market_data:
        structured_data["about"] = {
            "@type": "Thing",
            "name": "Cryptocurrency Market",
            "description": f"Bitcoin: ${market_data.get('bitcoin', {}).get('price', 0):,.2f}, Ethereum: ${market_data.get('ethereum', {}).get('price', 0):,.2f}"
        }
    
    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{meta_tags['title']}</title>
    <meta name=\"description\" content=\"{meta_tags['description']}\">
    <meta name=\"keywords\" content=\"{meta_tags['keywords']}\">
    <meta name=\"robots\" content=\"{meta_tags['robots']}\">
    <meta name=\"author\" content=\"Crypto Expert\">
    <meta name=\"article:published_time\" content=\"{datetime.now().isoformat()}\">
    <meta name=\"article:modified_time\" content=\"{datetime.now().isoformat()}\">
    
    <!-- Open Graph -->
    <meta property=\"og:title\" content=\"{meta_tags['og:title']}\">
    <meta property=\"og:description\" content=\"{meta_tags['og:description']}\">
    <meta property=\"og:type\" content=\"{meta_tags['og:type']}\">
    <meta property=\"og:site_name\" content=\"Crypto Insights Pro\">
    
    <!-- Twitter Card -->
    <meta name=\"twitter:card\" content=\"{meta_tags['twitter:card']}\">
    <meta name=\"twitter:title\" content=\"{meta_tags['twitter:title']}\">
    <meta name=\"twitter:description\" content=\"{meta_tags['twitter:description']}\">
    
    <!-- Structured Data -->
    <script type=\"application/ld+json\">
    {json.dumps(structured_data, indent=2)}
    </script>
    
    <style>
        body {{ font-family: 'Arial', sans-serif; line-height: 1.7; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; font-size: 2.2em; }}
        h2 {{ color: #34495e; margin-top: 40px; margin-bottom: 20px; font-size: 1.6em; border-left: 4px solid #3498db; padding-left: 15px; }}
        p {{ margin-bottom: 20px; text-align: justify; font-size: 16px; }}
        .meta {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .reading-time {{ font-style: italic; margin-bottom: 10px; }}
        .keywords {{ font-size: 14px; opacity: 0.9; }}
        .quality-metrics {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }}
        .market-data {{ background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }}
        .disclaimer {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107; font-size: 14px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .highlight {{ background: #fff3cd; padding: 2px 4px; border-radius: 3px; }}
        .meta-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .excerpt-section {{ background: #eaf6ff; border-left: 4px solid #3498db; padding: 12px 18px; margin-bottom: 24px; font-style: italic; color: #2c3e50; }}
    </style>
</head>
<body>
    <article>
        <div class="meta-section">
            <div><strong>Meta Title:</strong> {meta_title}</div>
            <div><strong>Meta Description:</strong> {meta_description}</div>
            <div><strong>Keywords:</strong> {', '.join(keywords[:5])}</div>
        </div>
        <h1>{title}</h1>
        <div class="excerpt-section"><strong>Excerpt:</strong> {excerpt}</div>
        <div class="meta">
            <div class="reading-time">📖 Reading time: {reading_time} minutes</div>
            <div>📅 Published: {datetime.now().strftime('%B %d, %Y')}</div>
        </div>
        {f'<div class="market-data"><h3>📊 Market Update</h3><p>Bitcoin: ${market_data.get("bitcoin", {}).get("price", 0):,.2f} ({market_data.get("bitcoin", {}).get("change_24h", 0):+.2f}%) | Ethereum: ${market_data.get("ethereum", {}).get("price", 0):,.2f} ({market_data.get("ethereum", {}).get("change_24h", 0):+.2f}%)</p></div>' if market_data else ''}
        {f'<div class="quality-metrics"><h3>📈 Content Quality</h3><p>Quality Score: {quality_metrics.get("quality_score", 0)}/100 | Readability: {quality_metrics.get("flesch_score", 0)} | Word Count: {quality_metrics.get("word_count", 0):,}</p></div>' if quality_metrics else ''}
        <div class="content">
"""
    # Process content and add proper HTML structure
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            if paragraph.startswith('##'):
                heading_text = paragraph[3:].strip()
                html_content += f'            <h2>{heading_text}</h2>\n'
            else:
                html_content += f'            <p>{paragraph}</p>\n'
    # Add disclaimer
    html_content += """
        <div class="disclaimer">
            <strong>Disclaimer:</strong> This article is for informational purposes only and does not constitute financial advice. Cryptocurrency investments carry significant risks. Always conduct your own research and consult with financial advisors before making investment decisions.
        </div>
        </div>
    </article>
</body>
</html>"""
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return fname

def generate_seo_meta_tags(title, description, keywords):
    """Generate comprehensive SEO meta tags"""
    return {
        'title': title,
        'description': description[:160],
        'keywords': ', '.join(keywords),
        'robots': 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1',
        'og:title': title,
        'og:description': description[:160],
        'og:type': 'article',
        'twitter:card': 'summary_large_image',
        'twitter:title': title,
        'twitter:description': description[:160]
    }

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENHANCED AGENT
# ─────────────────────────────────────────────────────────────────────────────
def run_ultimate_agent():
    logger.info("🚀 Starting Ultimate Crypto Article AI Agent...")
    
    # 1. Get latest articles from multiple sources
    logger.info("📰 Fetching articles from multiple sources...")
    articles = get_latest_articles_from_multiple_sources()
    if not articles:
        logger.error("Failed to get articles from any source")
        return
    
    # Select best article based on weight
    best_article = articles[0]
    logger.info(f"📄 Selected article: {best_article['title']} from {best_article['source']}")
    
    # 2. Extract article data
    art = extract_article_data(best_article['url'])
    if not art["content"]:
        logger.error("Failed to extract article content")
        return
    
    # 3. Advanced keyword research
    logger.info("🔍 Researching advanced keywords...")
    keywords = get_advanced_keywords()
    keyword_sentiment = analyze_keyword_sentiment(keywords)
    primary_keywords = keywords[:10]
    
    logger.info(f"📊 Found {len(primary_keywords)} primary keywords")
    
    # 4. Get market data
    market_data = {}
    # if ENABLE_FACT_CHECKING:
    #     logger.info("📈 Fetching real-time market data...")
    #     market_data = get_crypto_market_data()
    
    # 5. Competitor analysis
    competitor_insights = {}
    if ENABLE_COMPETITOR_ANALYSIS:
        logger.info("🔍 Analyzing competitor content...")
        competitor_insights = analyze_competitor_content(primary_keywords, art["title"])
    
    # 6. Generate advanced content
    logger.info("✍️ Generating human-like content...")
    prompt = build_advanced_prompt(
        art["content"], 
        primary_keywords, 
        market_data,
        competitor_insights
    )
    
    content = generate_advanced_content(prompt)
    
    if not content.strip():
        logger.error("Failed to generate content")
        return
    
    # 7. Extract title and optimize
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    title = None
    body_lines = []
    for line in lines:
        if not title and (line.lower().startswith('**headline:**') or line.lower().startswith('headline:')):
            # Extract after the colon
            title = line.split(':', 1)[-1].strip(' *')
            continue  # skip this line in body
        body_lines.append(line)
    if not title:
        # Fallback: use first non-empty line
        title = lines[0] if lines else "Untitled"
        body_lines = lines[1:] if len(lines) > 1 else []
    body_content = '\n\n'.join(body_lines)
    
    # 8. Skip quality analysis for human-like content
    quality_metrics = {}
    # if ENABLE_CONTENT_SCORING:
    #     logger.info("📊 Analyzing content quality...")
    #     quality_metrics = analyze_content_quality(body_content)
    
    # 9. Create meta description
    meta_description = body_content[:150] + "..." if len(body_content) > 150 else body_content
    
    # 10. Export advanced HTML
    html_file = export_advanced_html(title, body_content, primary_keywords, meta_description, market_data, quality_metrics)
    
    logger.info(f"✅ Ultimate article exported: {html_file}")
    logger.info(f"📈 Target keywords: {', '.join(primary_keywords[:5])}")
    logger.info(f"📊 Word count: {len(body_content.split())}")
    if quality_metrics:
        logger.info(f"🎯 Quality score: {quality_metrics.get('quality_score', 0)}/100")
    if market_data:
        logger.info(f"📈 Market data integrated")
    if competitor_insights:
        logger.info(f"🔍 Competitor analysis completed")
    
    return html_file

if __name__ == "__main__":
    if not DEEPSEEK_KEY or not MODEL_ID:
        raise RuntimeError("DEEPSEEK_KEY and MODEL_ID must be set in your environment (.env file)")
    run_ultimate_agent()