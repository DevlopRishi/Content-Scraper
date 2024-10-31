# Content Scraper and Formatter

A comprehensive tool to scrape and format content from websites, YouTube videos, and PDFs, specifically designed for collecting and formatting teachings.

## Features

- Web scraping from any website including subpages
- YouTube channel/video content extraction
- PDF content extraction
- Automatic formatting to JSON
- Modern web interface
- Integration with Google's Gemini API for enhanced text formatting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DevlopRishi/content-scraper
cd content-scraper
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Add your Gemini API key to .env file
```

## Backend Setup (Python)

The backend uses FastAPI to handle scraping requests. Install additional dependencies:

```bash
pip install fastapi uvicorn youtube-dl beautifulsoup4 PyPDF2 google-generativeai
```

Start the backend server:
```bash
uvicorn main:app --reload
```

## Frontend Setup

Start the development server:
```bash
npm run dev
```

## Usage

1. Access the web interface at `http://localhost:3000`

2. Choose the type of content to scrape:
   - Website: Enter the main URL to scrape all subpages
   - YouTube: Enter channel URL to scrape all videos
   - PDF: Enter PDF URL or upload PDF files

3. Click "Start Scraping" to begin the process

4. Download the formatted JSON files when complete

## File Structure

```
content-scraper/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   ├── public/
│   └── package.json
├── backend/
│   ├── scrapers/
│   │   ├── website_scraper.py
│   │   ├── youtube_scraper.py
│   │   └── pdf_scraper.py
│   ├── formatters/
│   │   └── gemini_formatter.py
│   └── main.py
└── README.md
```

## API Documentation

### Website Scraping
```python
POST /api/scrape/website
{
    "url": "https://example.com",
    "depth": 2  // How many levels of subpages to scrape
}
```

### YouTube Scraping
```python
POST /api/scrape/youtube
{
    "url": "https://youtube.com/channel/...",
    "max_videos": 100  // Maximum number of videos to scrape
}
```

### PDF Processing
```python
POST /api/scrape/pdf
{
    "url": "https://example.com/document.pdf"
}
```

## Gemini API Integration

The project uses Google's Gemini API for enhanced text formatting. Format text using:

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

response = genai.generate_text(
    "Format the following content into a Q&A pair: " + content
)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
