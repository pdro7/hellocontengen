# HelloPrint Multilingual Content Generator

A Python-based pipeline that generates multilingual marketing content using OpenAI GPT and publishes to Contentful CMS.

## Core Features

- **Multilingual Generation**: Creates content in English, Dutch and Portuguese
- **Language Validation**: Ensures content is properly localized using OpenAI
- **CMS Integration**: Publishes draft entries to Contentful
- **Structured Logging**: JSON-formatted execution logs

## Project Structure

```
HelloPrint/
├── ai_client.py           # OpenAI integration for content generation
├── contentful_client.py   # Contentful CMS API client
├── keywords.csv          # Input keywords for content generation
├── content_validator.py     # Language validation using OpenAI
├── logging_setup.py      # JSON logging configuration
├── pipeline.py           # Core pipeline orchestration
├── products.csv         # Product data for content generation
├── run_pipeline.py      # Main execution script
├── templates.py         # Basic content templates

```

## Setup

### Requirements
- Python 3.8+
- Dependencies:
```sh
pip install openai requests jinja2 python-dotenv tenacity
```

### Configuration
Create `.env` file with:
```ini
OPENAI_API_KEY=your-key
CONTENTFUL_SPACE_ID=your-space
CONTENTFUL_ENVIRONMENT=master
CONTENTFUL_ACCESS_TOKEN=your-token
```

## Usage

1. Update input data:
   - `products.csv`: Product catalog
   - `keywords.csv`: Target keywords by locale

2. Run pipeline:
```sh
python run_pipeline.py
```

3. Check Contentful for generated drafts

## Technical Details

### Content Model
- Content type: `marketingContent`
- Fields:
  - title (localized)
  - body (localized) 
  - slug (auto-generated)
  - keywords
  - category

### Supported Locales
- English (en_US)
- Dutch (nl_NL) 
- Portuguese (pt_BR)

### Error Handling
- Automatic retries for API calls
- Language validation per locale
- JSON-formatted error logs

### Logging
- Location: `logs/pipeline.json`
- Format: Structured JSON
- Fields: timestamp, locale, status, errors

## Customization

- Content templates: `templates2.py`
- Validation rules: `lang_validator.py`
- Product data: `products.csv`
- Keywords: `keywords.csv`

## License

MIT