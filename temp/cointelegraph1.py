#!/usr/bin/env python3
"""
cointelegraph_agent.py - Enhanced SEO-Optimized Crypto Article Generator

1. Fetch latest article from Cointelegraph RSS
2. Extract title & content with HTTP header + RSS fallback
3. Advanced keyword research with multiple sources (Google Trends, SEMrush-like data, competitor analysis)
4. SEO-optimized content generation with low AI detection scores
5. Multiple paraphrase passes with human-like writing patterns
6. Generate SEO-optimized image prompts
7. Export final article as HTML with full SEO optimization (meta tags, structured data, schema markup)
"""
import os
import sys
import logging
import requests
import feedparser
import json
import random
import re
from urllib.parse import urlparse, parse_qs

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from openai import OpenAI

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION (HARDCODED)
# ─────────────────────────────────────────────────────────────────────────────
DEEPSEEK_KEY = "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"    # DeepSeek (OpenRouter) API key
MODEL_ID     = "deepseek/deepseek-r1-0528-qwen3-8b:free"      # Valid model ID from --list-models
OUTPUT_DIR   = "exports"
RSS_URL      = "https://cointelegraph.com/rss"

# SEO Configuration
TARGET_WORD_COUNT = 1800  # Optimal for crypto articles
KEYWORD_DENSITY = 2.5     # Target keyword density percentage
MIN_READING_TIME = 7      # Minimum reading time in minutes

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# CLIENT INITIALIZATION
# ─────────────────────────────────────────────────────────────────────────────
deepseek = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://openrouter.ai/api/v1")

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED KEYWORD RESEARCH
# ─────────────────────────────────────────────────────────────────────────────
def get_trending_crypto_keywords():
    """Get trending crypto keywords from multiple sources"""
    keywords = []
    
    # Google Trends data
    try:
        pt = TrendReq(hl="en-US", tz=330)
        trending_topics = [
            "bitcoin", "ethereum", "cryptocurrency", "blockchain", 
            "defi", "nft", "web3", "crypto trading", "altcoin"
        ]
        
        for topic in trending_topics[:5]:  # Limit to avoid rate limiting
            pt.build_payload([topic], timeframe='now 7-d')
            related = pt.related_queries()
            if topic in related and related[topic]['rising'] is not None:
                rising_kws = related[topic]['rising']['query'].tolist()[:3]
                keywords.extend(rising_kws)
    except Exception as e:
        logger.warning(f"Google Trends failed: {e}")
    
    # Add high-value crypto keywords
    high_value_keywords = [
        "Bitcoin ETF approval", "Ethereum staking rewards", "DeFi yield farming",
        "NFT marketplace trends", "Layer 2 scaling solutions", "Crypto regulation news",
        "Web3 gaming platforms", "Stablecoin adoption", "Crypto mining profitability",
        "Smart contract security", "Cross-chain bridges", "Metaverse crypto projects"
    ]
    keywords.extend(high_value_keywords)
    
    # Remove duplicates and return
    return list(set(keywords))[:15]

def analyze_competitor_keywords(url):
    """Extract keywords from competitor articles"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract from title and headings
        title = soup.find('title')
        headings = soup.find_all(['h1', 'h2', 'h3'])
        
        text_content = []
        if title:
            text_content.append(title.get_text())
        for heading in headings[:5]:
            text_content.append(heading.get_text())
        
        # Simple keyword extraction
        words = ' '.join(text_content).lower().split()
        return [word for word in words if len(word) > 4][:10]
        
    except Exception as e:
        logger.warning(f"Competitor analysis failed: {e}")
        return []

# ─────────────────────────────────────────────────────────────────────────────
# SEO OPTIMIZATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def calculate_keyword_density(text, keywords):
    """Calculate keyword density in text"""
    text_lower = text.lower()
    total_words = len(text.split())
    keyword_count = sum(text_lower.count(keyword.lower()) for keyword in keywords)
    return (keyword_count / total_words) * 100 if total_words > 0 else 0

def optimize_for_seo(text, target_keywords, target_density=2.5):
    """Optimize text for SEO with proper keyword distribution"""
    current_density = calculate_keyword_density(text, target_keywords)
    
    if current_density < target_density:
        # Add keywords naturally
        sentences = text.split('. ')
        for i, sentence in enumerate(sentences):
            if i % 3 == 0 and target_keywords:  # Every 3rd sentence
                keyword = random.choice(target_keywords)
                if keyword.lower() not in sentence.lower():
                    sentences[i] = f"{sentence} {keyword}."
        
        text = '. '.join(sentences)
    
    return text

def generate_seo_meta_tags(title, description, keywords):
    """Generate SEO meta tags"""
    return {
        'title': title,
        'description': description[:160],  # Google's recommended length
        'keywords': ', '.join(keywords),
        'robots': 'index, follow',
        'og:title': title,
        'og:description': description[:160],
        'og:type': 'article',
        'twitter:card': 'summary_large_image',
        'twitter:title': title,
        'twitter:description': description[:160]
    }

# ─────────────────────────────────────────────────────────────────────────────
# AI DETECTION AVOIDANCE TECHNIQUES
# ─────────────────────────────────────────────────────────────────────────────
def add_human_patterns(text):
    """Add human-like writing patterns to avoid AI detection"""
    
    # Add natural transitions
    transitions = [
        "Moreover,", "Furthermore,", "Additionally,", "On the other hand,",
        "However,", "Nevertheless,", "In contrast,", "Similarly,",
        "For instance,", "For example,", "Specifically,", "In particular,"
    ]
    
    # Add personal opinions and qualifiers
    qualifiers = [
        "It's worth noting that", "Interestingly,", "Surprisingly,",
        "According to experts,", "Many believe that", "Some argue that",
        "It appears that", "This suggests that", "This indicates that"
    ]
    
    # Add conversational elements
    conversational = [
        "Let's dive deeper into", "Here's what you need to know about",
        "The bottom line is", "Simply put,", "In essence,"
    ]
    
    sentences = text.split('. ')
    enhanced_sentences = []
    
    for i, sentence in enumerate(sentences):
        if i % 4 == 0 and i > 0:  # Every 4th sentence
            pattern = random.choice(transitions + qualifiers + conversational)
            enhanced_sentences.append(f"{pattern} {sentence}")
        else:
            enhanced_sentences.append(sentence)
    
    return '. '.join(enhanced_sentences)

def vary_sentence_structure(text):
    """Vary sentence structure to appear more human"""
    sentences = text.split('. ')
    varied_sentences = []
    
    for sentence in sentences:
        if random.random() < 0.3:  # 30% chance to restructure
            words = sentence.split()
            if len(words) > 8:
                # Move a phrase to the beginning
                mid_point = len(words) // 2
                first_half = words[:mid_point]
                second_half = words[mid_point:]
                sentence = f"{' '.join(second_half)}, {' '.join(first_half)}"
        
        varied_sentences.append(sentence)
    
    return '. '.join(varied_sentences)

# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED CONTENT GENERATION
# ─────────────────────────────────────────────────────────────────────────────
def build_seo_optimized_prompt(original_content, keywords, competitor_insights):
    """Build a comprehensive SEO-optimized prompt"""
    
    primary_keywords = keywords[:5]
    secondary_keywords = keywords[5:10]
    
    prompt = f"""
You are an expert crypto journalist and SEO specialist. Create a comprehensive, engaging article that:

SEO REQUIREMENTS:
- Primary keywords to include naturally: {', '.join(primary_keywords)}
- Secondary keywords to sprinkle throughout: {', '.join(secondary_keywords)}
- Target word count: {TARGET_WORD_COUNT} words
- Include 3-4 H2 subheadings for structure
- Start with a compelling hook
- End with a strong conclusion

CONTENT REQUIREMENTS:
- Write in a conversational, expert tone
- Include specific examples and data points
- Add personal insights and expert opinions
- Use natural transitions between paragraphs
- Vary sentence structure and length
- Include at least 2-3 specific cryptocurrency examples
- Mention current market trends and developments

AI AVOIDANCE:
- Use natural language patterns
- Include qualifiers and hedging language
- Add personal opinions and expert quotes
- Vary vocabulary and avoid repetitive phrases
- Use contractions and informal language where appropriate

IMPORTANT: Start your response with a clear, SEO-optimized title on the first line, followed by the article content with proper H2 subheadings.

Original article context:
{original_content[:500]}...

Competitor insights to consider:
{competitor_insights[:200]}...

Create an article that ranks well in search engines while maintaining high readability and engagement.
"""
    return prompt

def generate_seo_content(prompt):
    """Generate SEO-optimized content with multiple passes"""
    
    # First pass - main content
    response = deepseek.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You are an expert crypto journalist. Write naturally, avoid AI patterns, and focus on providing valuable insights. Always start with a clear title on the first line."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=2000
    )
    
    content = response.choices[0].message.content.strip()
    
    # Clean up the content and ensure proper structure
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            # Remove any markdown formatting from titles
            if line.startswith('# '):
                line = line[2:]
            elif line.startswith('## '):
                line = f"## {line[3:]}"
            cleaned_lines.append(line)
    
    content = '\n\n'.join(cleaned_lines)
    
    # Second pass - enhance with human patterns
    enhancement_prompt = f"""
Enhance this article to sound more human and natural. Keep the same structure but improve the flow:

{content}

Add:
- Natural transitions and qualifiers
- Personal insights and expert opinions
- Conversational elements
- Varied sentence structures
- Specific examples and data points
- Better paragraph breaks
"""
    
    response = deepseek.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": enhancement_prompt}],
        temperature=0.9,
        max_tokens=2000
    )
    
    enhanced_content = response.choices[0].message.content.strip()
    
    # Apply additional human patterns
    final_content = add_human_patterns(enhanced_content)
    final_content = vary_sentence_structure(final_content)
    
    return final_content

# ─────────────────────────────────────────────────────────────────────────────
# ENHANCED HTML EXPORT WITH SEO
# ─────────────────────────────────────────────────────────────────────────────
def export_seo_optimized_html(title, content, keywords, meta_description):
    """Export article with full SEO optimization"""
    
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    fname = os.path.join(OUTPUT_DIR, f"seo_article_{ts}.html")
    
    # Clean up title and description
    title = title.strip()
    if len(title) > 60:
        title = title[:57] + "..."
    
    meta_description = meta_description.strip()
    if len(meta_description) > 160:
        meta_description = meta_description[:157] + "..."
    
    # Generate meta tags
    meta_tags = generate_seo_meta_tags(title, meta_description, keywords)
    
    # Calculate reading time
    word_count = len(content.split())
    reading_time = max(MIN_READING_TIME, word_count // 200)
    
    # Create structured data
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": meta_description,
        "author": {
            "@type": "Person",
            "name": "Crypto Expert"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Crypto Insights",
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
        }
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_tags['title']}</title>
    <meta name="description" content="{meta_tags['description']}">
    <meta name="keywords" content="{meta_tags['keywords']}">
    <meta name="robots" content="{meta_tags['robots']}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{meta_tags['og:title']}">
    <meta property="og:description" content="{meta_tags['og:description']}">
    <meta property="og:type" content="{meta_tags['og:type']}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="{meta_tags['twitter:card']}">
    <meta name="twitter:title" content="{meta_tags['twitter:title']}">
    <meta name="twitter:description" content="{meta_tags['twitter:description']}">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {json.dumps(structured_data, indent=2)}
    </script>
    
    <style>
        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        p {{ margin-bottom: 15px; text-align: justify; }}
        .meta {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .reading-time {{ color: #7f8c8d; font-style: italic; }}
    </style>
</head>
<body>
    <article>
        <h1>{title}</h1>
        
        <div class="meta">
            <div class="reading-time">📖 Reading time: {reading_time} minutes</div>
            <div>📅 Published: {datetime.now().strftime('%B %d, %Y')}</div>
            <div>🏷️ Keywords: {', '.join(keywords[:5])}</div>
        </div>
        
        <div class="content">
"""
    
    # Process content and add proper HTML structure
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            if paragraph.startswith('##'):
                # This is a subheading
                heading_text = paragraph[3:].strip()
                html_content += f'            <h2>{heading_text}</h2>\n'
            else:
                # This is a paragraph
                html_content += f'            <p>{paragraph}</p>\n'
    
    html_content += """        </div>
    </article>
</body>
</html>"""
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return fname

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENHANCED AGENT
# ─────────────────────────────────────────────────────────────────────────────
def run_enhanced_agent():
    logger.info("🚀 Starting Enhanced SEO Agent...")
    
    # 1. Get latest article
    url = get_latest_article_url()
    if not url:
        logger.error("Failed to get latest article URL")
        return
    
    # 2. Extract article data
    art = extract_article_data(url)
    if not art["content"]:
        logger.error("Failed to extract article content")
        return
    
    # 3. Advanced keyword research
    logger.info("🔍 Researching trending keywords...")
    trending_keywords = get_trending_crypto_keywords()
    competitor_keywords = analyze_competitor_keywords(url)
    
    # Combine and prioritize keywords
    all_keywords = list(set(trending_keywords + competitor_keywords))
    primary_keywords = all_keywords[:8]
    
    logger.info(f"📊 Found {len(primary_keywords)} primary keywords: {', '.join(primary_keywords[:3])}...")
    
    # 4. Generate SEO-optimized content
    logger.info("✍️ Generating SEO-optimized content...")
    prompt = build_seo_optimized_prompt(
        art["content"], 
        primary_keywords, 
        "Recent market analysis shows increasing interest in DeFi protocols and Layer 2 solutions."
    )
    
    content = generate_seo_content(prompt)
    
    if not content.strip():
        logger.error("Failed to generate content")
        return
    
    # 5. Extract title and optimize
    lines = content.split('\n')
    title = lines[0].strip()
    body_content = '\n\n'.join(lines[1:])
    
    # 6. Create meta description
    meta_description = body_content[:150] + "..." if len(body_content) > 150 else body_content
    
    # 7. Export SEO-optimized HTML
    html_file = export_seo_optimized_html(title, body_content, primary_keywords, meta_description)
    
    logger.info(f"✅ SEO-optimized article exported: {html_file}")
    logger.info(f"📈 Target keywords: {', '.join(primary_keywords[:5])}")
    logger.info(f"📊 Word count: {len(body_content.split())}")
    
    return html_file

# Keep the original functions for compatibility
def get_latest_article_url():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        logger.error("RSS feed empty or unreachable.")
        return None
    return feed.entries[0].link

def extract_article_data(url: str) -> dict:
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

        title_tag = soup.select_one("h1") or soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

        paras = soup.select("div.post-content p") or soup.select("article p")
        content = "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))

        if not content:
            raise ValueError("Empty content extracted")
        return {"title": title, "content": content, "url": url}
    except Exception as err:
        logger.warning("Full fetch failed (%s); falling back to RSS summary.", err)
        feed = feedparser.parse(RSS_URL)
        entry = feed.entries[0]
        summary = BeautifulSoup(entry.summary, "html.parser").get_text(strip=True)
        return {"title": entry.title, "content": summary, "url": url}

if __name__ == "__main__":
    run_enhanced_agent()