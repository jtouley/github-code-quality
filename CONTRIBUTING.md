# Contributing to GitHub Code Quality Analyzer

Thank you for your interest in contributing to this project! Here's how to get started.

## Development Setup

1. Fork and clone the repository:
   ```sh
   git clone https://github.com/your-username/github-code-quality.git
   cd github-code-quality
   ```

2. Set up the development environment:
   ```sh
   bash config/setup.sh
   ```

3. Create a `.env` file with your API keys:
   ```sh
   cp .env.example .env
   # Edit .env with your actual keys
   ```

## Testing Your Changes

### Testing Locally with act

[act](https://github.com/nektos/act) allows you to run GitHub Actions locally:

1. Create a `.secrets` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_TOKEN=your_github_token_here
   ```

2. Test the action:
   ```sh
   act -j analyze-code --secret-file .secrets
   ```

3. On Apple Silicon Macs:
   ```sh
   act -j analyze-code --secret-file .secrets --container-architecture linux/amd64
   ```

### Docker Testing

You can also test the Docker image directly:

```bash
# Build the image
docker build -t code-quality-analyzer .

# Run with your API keys
docker run -e INPUT_REPO="owner/repo" -e INPUT_OPENAI_API_KEY="your_key" -e INPUT_GITHUB_TOKEN="your_token" code-quality-analyzer
```

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Test your changes locally using act
4. Submit a pull request

## Action Structure

- `action.yml` - GitHub Action definition
- `Dockerfile` - Container definition
- `entrypoint.sh` - Script that runs when the container starts
- `src/` - Python code for analysis
  - `analyzer.py` - Main analyzer module
  - `ai_client.py` - OpenAI integration
  - `github_client.py` - GitHub API integration
  - `config_loader.py` - Configuration management
  - `post_comment.py` - PR comment integration
  - `utils.py` - Utility functions

## Code Style

This project uses:
- Black for code formatting
- Flake8 for style checking
- Pre-commit hooks to enforce code quality

Make sure your code passes all checks before submitting a PR:
```sh
pre-commit run --all-files
```

## Testing

Run tests to ensure your changes don't break existing functionality:
```sh
pytest tests/
```

## Documentation

Please update documentation when making changes to:
- Configuration options
- CLI usage
- Core functionality
- Installation process

## Submitting Changes

1. Push your changes to your forked repository
2. Create a pull request to the main repository
3. Describe your changes and the problem they solve
4. Reference any related issues

Thank you for contributing to making code more DRY and SOLID!