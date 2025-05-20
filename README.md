# HelloPrint Product Description draft Content Generator for Contentful

A Python-based pipeline that generates multilingual marketing content for products using OpenAI and publishes to Contentful CMS.

## Project Overview

This pipeline automates the creation of product marketing content in multiple languages:
- Generates SEO-optimized product descriptions based on keywords
- Validates that content is properly localized in target languages
- Publishes drafts to Contentful CMS
- Tracks execution with structured JSON logging

## Project Structure

```
HelloPrint/
├── src/                   # Source code directory
│   ├── ai_client.py       # OpenAI API integration
│   ├── contentful_client.py # Contentful CMS publishing client
│   ├── content_validator.py # Content validation utilities
│   ├── lang_validator.py  # Language validation using OpenAI
│   ├── logging_setup.py   # JSON logging configuration
│   ├── pipeline.py        # Core data loading and processing
│   ├── run_pipeline.py    # Main execution script
│   └── templates_loader.py # Template loading utilities
├── data/                  # Data directory
│   ├── keywords.csv       # Target keywords for content generation
│   └── products.csv       # Product information data
├── tests/                 # Test directory
│   └── test_validator.py  # Unit tests for content validation
├── logs/                  # Logging directory
│   └── pipeline.json      # Pipeline execution logs
└── templates/             # Content generation templates
    └── prompts.jinja      # Jinja2 templates for AI prompts
```

## Setup

### Requirements
- Python 3.8+
- Required packages:
  ```
  openai
  requests
  python-dotenv
  tenacity
  jinja2
  pytest (for testing)
  ```

### Configuration
Create a `.env` file in the project root with:
```
OPENAI_API_KEY="your_api_key"
CONTENTFUL_SPACE_ID="your_space_id"
CONTENTFUL_ENVIRONMENT="master"
CONTENTFUL_ACCESS_TOKEN="your_access_token"
```

## Usage

1. **Prepare Input Data**
   - Update `data/products.csv` with product information
   - Modify `data/keywords.csv` with target keywords per locale

2. **Run Pipeline**
   ```
   python src/run_pipeline.py
   ```

3. **View Results**
   - Check Contentful for created draft entries
   - Review logs in `logs/pipeline.json`

## Technical Details

### AI Content Generation
- Uses OpenAI's GPT-4o-mini model
- Structured JSON output format for consistent content
- Retry mechanism for API reliability
- Language validation to ensure proper localization

### Content Validation
- Title length check (maximum 60 characters)
- Keyword presence verification
- Language validation to ensure proper localization

### Contentful Integration
- Creates entries of type `productDescription`
- Populates multilingual fields (title, body, slug, keywords, category)
- Generates SEO-friendly slugs from keywords
- Error handling with detailed logging

### Supported Languages
- English (en_US)
- Dutch (nl_NL)
- Portuguese (pt_BR)

### Template Loading
- Dynamic loading of Jinja2 templates via `templates_loader.py`
- Support for customizable prompt templates
- Separation of template logic from content generation

### Data Processing
- Keywords selection based on locale
- Product catalog processing
- Slug generation and normalization

## Customization

- **Products**: Update `data/products.csv` with custom product information
- **Keywords**: Modify `data/keywords.csv` to target specific SEO terms
- **Templates**: Adjust AI prompts in `templates/prompts.jinja`
- **Locales**: Configure supported languages in `src/run_pipeline.py`
- **Content Model**: Adjust field mapping in `src/contentful_client.py`

## Code Structure Notes

The project follows a modular structure:
- `src/pipeline.py` handles data processing and keyword selection
- `src/ai_client.py` manages OpenAI API interaction
- `src/contentful_client.py` handles CMS publishing
- `src/lang_validator.py` ensures proper content localization
- `src/run_pipeline.py` orchestrates the entire workflow

## Validation
Validation rules in `src/content_validator.py`

## Testing

Run the test suite with:
```
pytest tests/
```

Tests verify:
- Content validation functions
- Title length constraints
- Keyword detection in content
- Language validation

## Logging

All operations are logged to `logs/pipeline.json` with:
- Timestamp
- Operation type
- Status (success/error)
- Content details (locale, keyword)
- Error messages (when applicable)

## Error Handling

- Automatic retries for API calls (using tenacity)
- Content validation to ensure quality
- Language validation to ensure content is in correct language
- Structured error messages in logs

## License

MIT



