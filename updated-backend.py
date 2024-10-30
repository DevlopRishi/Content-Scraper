# backend/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
from datetime import datetime

# Import scrapers
from scrapers.enhanced_website_scraper import EnhancedWebsiteScraper
from scrapers.youtube_scraper import YouTubeScraper
from scrapers.pdf_scraper import PDFScraper
from formatters.gemini_formatter import GeminiFormatter

app = FastAPI()

# Configure CORS for Netlify deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Netlify domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ScrapeRequest(BaseModel):
    url: str
    depth: int = 2
    max_pages: int = 100
    max_workers: int = 5
    include_subdomains: bool = True

class ScrapeResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Store for background tasks
task_store = {}

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def update_task_status(task_id: str, status: str, result: Optional[dict] = None):
    if task_id in task_store:
        task_store[task_id].update({
            "status": status,
            "updated_at": datetime.now().isoformat(),
            "result": result
        })

async def process_website(task_id: str, request: ScrapeRequest):
    try:
        # Initialize scrapers
        website_scraper = EnhancedWebsiteScraper()
        formatter = GeminiFormatter()
        
        update_task_status(task_id, "SCRAPING")
        
        # Scrape website
        results = website_scraper.scrape_site(
            start_url=request.url,
            max_pages=request.max_pages,
            max_workers=request.max_workers
        )
        
        update_task_status(task_id, "FORMATTING")
        
        # Format content using Gemini
        formatted_results = []
        for page in results['results']:
            if page['text']:
                formatted_content = formatter.format_content(page['text'])
                if formatted_content:
                    formatted_results.append({
                        'url': page['url'],
                        'formatted_content': formatted_content
                    })
        
        # Save results
        timestamp = get_timestamp()
        filename = f"scraped_content_{task_id}_{timestamp}.json"
        output_path = os.path.join('downloads', filename)
        
        os.makedirs('downloads', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'url': request.url,
                    'pages_scraped': results['pages_scraped'],
                    'timestamp': timestamp
                },
                'results': formatted_results
            }, f, indent=2, ensure_ascii=False)
        
        update_task_status(task_id, "COMPLETED", {
            'download_url': f"/downloads/{filename}",
            'pages_scraped': results['pages_scraped']
        })
        
    except Exception as e:
        update_task_status(task_id, "FAILED", {'error': str(e)})

@app.post("/api/scrape/website", response_model=ScrapeResponse)
async def scrape_website(request: ScrapeRequest, background_tasks: BackgroundTasks):
    task_id = f"task_{get_timestamp()}"
    task_store[task_id] = {
        "status": "PENDING",
        "created_at": datetime.now().isoformat(),
        "type": "website",
        "url": request.url
    }
    
    background_tasks.add_task(process_website, task_id, request)
    
    return ScrapeResponse(
        task_id=task_id,
        status="PENDING",
        message="Scraping task started"
    )

@app.get("/api/task/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in task_store:
        raise HTTPException(status_code=404, message="Task not found")
    
    return task_store[task_id]

@app.post("/api/scrape/youtube")
async def scrape_youtube(request: ScrapeRequest, background_tasks: BackgroundTasks):
    # Similar implementation for YouTube scraping
    pass

@app.post("/api/scrape/pdf")
async def scrape_pdf(request: ScrapeRequest, background_tasks: BackgroundTasks):
    # Similar implementation for PDF scraping
    pass

# Additional utility endpoints
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)