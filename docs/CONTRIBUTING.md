# Contributing to LinkedIn Scraper MCP Server

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/linkedin-scraper-mcp.git
   cd linkedin-scraper-mcp
   ```
3. **Set up the development environment**:
   ```bash
   bash install.sh
   # or
   make install
   ```

## Development Workflow

### 1. Create a Branch

Create a feature branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation changes
- `refactor/` for code refactoring

### 2. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update tests as needed
- Update documentation if applicable

### 3. Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Format your code before committing:

```bash
make format
make lint
```

### 4. Testing

Run tests to ensure your changes don't break existing functionality:

```bash
make test
```

Write new tests for new features:
- Place tests in `tests/` directory
- Follow existing test patterns
- Aim for high test coverage

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add job filtering by salary range"
```

Commit message format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding or updating tests
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots (if applicable)

## Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

Example:

```python
def scrape_profile(self, profile_url: str) -> Dict[str, Any]:
    """
    Scrape a LinkedIn profile.
    
    Args:
        profile_url: LinkedIn profile URL
        
    Returns:
        Dictionary containing profile information
        
    Raises:
        ValueError: If URL is invalid
    """
    # Implementation
    pass
```

### Error Handling

- Use appropriate exception types
- Provide clear error messages
- Log errors appropriately
- Handle rate limiting gracefully

### Rate Limiting

- Respect LinkedIn's rate limits
- Add appropriate delays between requests
- Implement exponential backoff for retries

## Project Structure

```
mcp/
├── src/              # Source code
│   ├── server.py     # MCP server
│   ├── scraper.py    # Scraping logic
│   └── utils.py      # Utilities
├── tests/            # Test files
├── examples/         # Example scripts
├── docs/             # Documentation
└── logs/             # Log files
```

## Adding New Features

### Adding a New Scraping Tool

1. Implement the scraping logic in `src/scraper.py`
2. Add the tool definition in `src/server.py` in `list_tools()`
3. Implement the tool handler in `call_tool()`
4. Add tests in `tests/test_scraper.py`
5. Update documentation in `README.md`

Example:

```python
# In src/scraper.py
@rate_limit(delay=2.0)
def scrape_posts(self, profile_id: str) -> List[Dict[str, Any]]:
    """Scrape posts from a profile."""
    # Implementation
    pass

# In src/server.py
Tool(
    name="scrape_linkedin_posts",
    description="Scrape recent posts from a LinkedIn profile",
    inputSchema={
        "type": "object",
        "properties": {
            "profile_id": {"type": "string", "description": "LinkedIn profile ID"},
        },
        "required": ["profile_id"],
    },
)
```

## Testing Guidelines

### Unit Tests

- Test individual functions in isolation
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests

- Test complete workflows
- Use test data that doesn't violate LinkedIn's ToS
- Clean up test data after tests

### Test Coverage

Aim for at least 80% test coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Include examples for complex functions

### README Updates

Update `README.md` when:
- Adding new features
- Changing installation process
- Modifying configuration options
- Adding new dependencies

## Security

### Credentials

- Never commit credentials or API keys
- Use environment variables for sensitive data
- Add credential files to `.gitignore`

### Data Privacy

- Respect LinkedIn's Terms of Service
- Don't store scraped data unnecessarily
- Implement data retention policies
- Follow GDPR and CCPA guidelines

## Performance

### Optimization

- Use async/await for I/O operations
- Implement caching where appropriate
- Minimize API calls
- Use batch operations when possible

### Rate Limiting

- Add delays between requests
- Implement exponential backoff
- Monitor rate limit headers
- Log rate limit violations

## Questions?

If you have questions or need help:
1. Check existing issues
2. Review documentation
3. Open a new issue with the `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better. Thank you for taking the time to contribute! 🎉

