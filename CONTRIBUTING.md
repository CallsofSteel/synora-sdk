# Contributing to Synora SDK

We love your input! We want to make contributing to Synora SDK as easy and transparent as possible.

## Development Process

We use GitHub to host code, track issues and feature requests, and accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

When you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project.

## Report bugs using GitHub's [issue tracker](https://github.com/synora/synora-sdk/issues)

We use GitHub issues to track public bugs. Report a bug by opening a new issue.

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

## Development Setup

### Python SDK

```bash
cd python
pip install -e ".[dev]"
pytest
```

### JavaScript SDK

```bash
cd javascript
npm install
npm test
```

## Coding Style

### Python
- Follow PEP 8
- Use type hints
- Use Black for formatting

### JavaScript/TypeScript
- Follow Airbnb style guide
- Use Prettier for formatting
- Use ESLint

## License

By contributing, you agree that your contributions will be licensed under its MIT License.