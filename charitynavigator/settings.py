# Scrapy settings for charitynavigator project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "charitynavigator"

SPIDER_MODULES = ["charitynavigator.spiders"]
NEWSPIDER_MODULE = "charitynavigator.spiders"

DEFAULT_REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'referer': 'https://www.charitynavigator.org/',
}



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "charitynavigator (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# High-performance settings with random delay
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 4

DOWNLOAD_DELAY = 0.2

# Random delay between 0.1 and 0.5 seconds
# DOWNLOAD_DELAY = 0.1
# RANDOMIZE_DOWNLOAD_DELAY = True  # This will multiply DOWNLOAD_DELAY by random value between 0.5 and 1.5

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': None,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': None,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': None,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {}

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 0.1  # Start with shorter delay
AUTOTHROTTLE_MAX_DELAY = 0.5    # Cap at half second
AUTOTHROTTLE_TARGET_CONCURRENCY = 16.0

# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 406, 408, 429]
RETRY_PRIORITY_ADJUST = -1

# Add compression handling
COMPRESSION_ENABLED = True
COMPRESSION_CODECS = {
    'gzip': 'scrapy.downloadermiddlewares.compression.GzipDecompressor',
    'deflate': 'scrapy.downloadermiddlewares.compression.DeflateDecompressor',
    'br': 'scrapy.downloadermiddlewares.compression.BrotliDecompressor',
}

# DNS settings for better performance
DNS_TIMEOUT = 10
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000

# Disable redirect middleware to handle them manually
REDIRECT_ENABLED = False

# Set a download timeout
DOWNLOAD_TIMEOUT = 15

# Enable memory usage debugging
MEMUSAGE_ENABLED = True
MEMUSAGE_WARNING_MB = 0
MEMUSAGE_LIMIT_MB = 2048
MEMUSAGE_CHECK_INTERVAL_SECONDS = 60

# Log settings
# LOG_LEVEL = 'INFO'
# LOG_ENABLED = True

# Disable loading of images, styles, and scripts
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
MEDIA_ALLOW_REDIRECTS = False

# Disable downloading of various media types
IMAGES_ENABLED = False
MEDIA_DOWNLOADS_ENABLED = False

# Explicitly disable specific handlers
DOWNLOAD_HANDLERS = {
    'image': None,
    'media': None,
}

# Disable caching
HTTPCACHE_ENABLED = False

# Queue settings
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'

# Try using Google or Cloudflare DNS
# DNS_RESOLVER = '8.8.8.8'  # Google DNS
