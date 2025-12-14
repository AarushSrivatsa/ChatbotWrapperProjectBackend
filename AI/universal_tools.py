from langchain_tavily import TavilySearch, TavilyCrawl, TavilyExtract
from langchain.tools import tool
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# SEARCH - Quick factual lookups (use this most)
search = TavilySearch(
    max_results=3,                    # Sweet spot - not too much noise
    topic="general",
    include_answer="basic",           # Get quick AI summary
    include_raw_content=False,        # Keep it fast
    include_images=True,              # Visual context is nice
    include_image_descriptions=False, # Not worth the cost
    search_depth="advanced",          # Better quality results
    # time_range="week",              # Uncomment if you want recent stuff
)

# CRAWL - Deep website exploration (use sparingly, expensive!)
crawl = TavilyCrawl(
    max_depth=3,                      # Don't go too deep
    max_breadth=15,                   # Reasonable breadth
    limit=20,                         # Stop before it gets crazy
    extract_depth="basic",            # "advanced" is overkill usually
    format="markdown",                # Easier to parse
    include_images=False,             # Keep it lean
    allow_external=False,             # Stay on target domain
)

# EXTRACT - Specific URL content (medium cost)
extract = TavilyExtract(
    extract_depth="advanced",         # Worth it for single URLs
    format="markdown",                # Better than text
    include_images=False,             # Usually not needed
)

@tool
def getDateAndTime():
    """Returns The Current Date & Time (Timezone IST)"""
    return datetime.now()

universal_tools = [getDateAndTime, search, crawl, extract]