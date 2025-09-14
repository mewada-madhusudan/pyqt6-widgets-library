# PyQt6 Widgets Library Documentation

This directory contains the comprehensive documentation for the PyQt6 Widgets Library.

## Documentation Structure

- **index.rst** - Main documentation index
- **installation.rst** - Installation guide and troubleshooting
- **quickstart.rst** - Quick start guide with examples
- **api/** - Complete API reference documentation
- **theming.rst** - Comprehensive theming guide
- **contributing.rst** - Contributing guidelines
- **changelog.rst** - Version history and migration guides
- **confluence_guide.md** - Confluence-style installation and usage guide

## Building Documentation

### Prerequisites

Install documentation dependencies:

```bash
pip install -r docs/requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be available in `_build/html/index.html`.

### Live Development

For live reloading during development:

```bash
cd docs
make livehtml
```

This will start a local server with auto-reload on file changes.

### Build for GitHub Pages

```bash
cd docs
make github
```

## Documentation Features

### API Reference
- Comprehensive widget documentation
- Parameter descriptions and examples
- Signal and method documentation
- Inheritance hierarchies

### Interactive Examples
- Code examples for all widgets
- Complete application examples
- Best practices and patterns

### Theming Guide
- Built-in theme documentation
- Custom theme creation
- Dynamic theme switching
- CSS integration

### Installation Guide
- Multiple installation methods
- Troubleshooting common issues
- Platform-specific instructions
- Virtual environment setup

## Contributing to Documentation

### Writing Guidelines

1. Use clear, concise language
2. Include practical examples
3. Follow RST formatting standards
4. Test all code examples
5. Update API documentation when adding features

### Documentation Standards

- Use Google-style docstrings in code
- Include parameter types and descriptions
- Provide usage examples
- Document signals and methods
- Add cross-references where appropriate

### Building and Testing

Before submitting documentation changes:

1. Build documentation locally
2. Check for warnings and errors
3. Test all code examples
4. Verify links and references
5. Review formatting and styling

## File Structure

```
docs/
├── _build/              # Built documentation (generated)
├── _static/             # Static assets (CSS, images)
├── _templates/          # Custom Sphinx templates
├── api/                 # API reference documentation
│   ├── index.rst
│   ├── base.rst
│   ├── cards.rst
│   ├── navigation.rst
│   ├── feedback.rst
│   ├── data.rst
│   ├── user.rst
│   ├── forms.rst
│   └── utility.rst
├── examples/            # Example applications and tutorials
├── conf.py              # Sphinx configuration
├── index.rst            # Main documentation index
├── installation.rst     # Installation guide
├── quickstart.rst       # Quick start tutorial
├── theming.rst          # Theming documentation
├── contributing.rst     # Contributing guidelines
├── changelog.rst        # Version history
├── confluence_guide.md  # Confluence-style guide
├── Makefile            # Build automation
├── requirements.txt    # Documentation dependencies
└── README.md           # This file
```

## Confluence Integration

The `confluence_guide.md` file is specifically formatted for Confluence wiki systems and includes:

- Installation instructions
- Widget usage examples
- Code snippets with syntax highlighting
- Troubleshooting guides
- Best practices

To use in Confluence:
1. Copy the content from `confluence_guide.md`
2. Paste into Confluence page editor
3. Confluence will automatically format the Markdown

## Maintenance

### Regular Updates

- Update API documentation when widgets change
- Add examples for new features
- Update installation instructions
- Maintain changelog with each release
- Review and update screenshots

### Quality Assurance

- Spell check all documentation
- Verify all links work correctly
- Test code examples in clean environment
- Ensure consistent formatting
- Check cross-references

## Support

For documentation issues:
- Open GitHub issues for errors or improvements
- Submit pull requests for corrections
- Participate in documentation discussions
- Help improve examples and tutorials