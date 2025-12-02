# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog/website built with Pelican static site generator, hosted on GitHub Pages. Content is written in Markdown (primarily in Obsidian) and includes blog posts about programming, machine learning, mathematics, and physics.

## Key Architecture

**Custom Obsidian Markdown Extension**: The core unique component is `obsidian_markdown.py`, a custom Markdown extension that converts Obsidian-style embeds (e.g., `![[image.png|Alt]]`) to HTML elements during the Pelican build. This allows seamless use of Obsidian's wiki-link syntax for images, audio, and video files.

- The extension resolves file paths by searching `content_root` and configured `static_dirs` (images, audio)
- Supports dimension specifications, alt text, titles, CSS classes, and inline styles
- Falls back to recursive search by filename if direct paths don't resolve
- Handles images (.png, .jpg, etc), audio (.mp3, .wav, etc), video (.mp4, .webm, etc), and generic file links

**Content Structure**:
- `content/`: Blog posts as Markdown files with Pelican metadata (Title, Date, Category, Status)
- `content/pages/`: Static pages (e.g., About)
- `content/images/`: Static images referenced in posts
- `content/audio/`: Audio files
- `templates/`: Markdown snippets (templates for common patterns like side-by-side images)
- `output/`: Generated static site (gitignored)

**Build Configuration**:
- `pelicanconf.py`: Development configuration (site name, paths, plugins, Markdown extensions)
- `publishconf.py`: Production settings (SITEURL, feeds, deletion of output directory)
- Pelican plugins: `pelican.plugins.render_math` for LaTeX math rendering

## Common Commands

**Build and serve locally**:
```bash
# Generate site with development settings
make html

# Serve with auto-reload during development
make devserver

# Or using invoke tasks
invoke serve          # Build and serve
invoke livereload     # Auto-reload on file changes
```

**Production deployment**:
```bash
# Generate production site
make publish

# Deploy to GitHub Pages (publishes to main branch)
make github
# Or: invoke gh-pages
```

**Clean output**:
```bash
make clean
# Or: invoke clean
```

## Development Notes

**Content files** follow this metadata format:
```markdown
Title: Post Title
Date: 2024-07-31 14:53
Category: Programming
Status: published
```

Status can be `published`, `draft`, or omitted.

**Static files** (images, audio) should be placed in `content/images/` or `content/audio/` and referenced using Obsidian-style embeds: `![[filename.png]]` or standard Pelican static file syntax: `{static}images/filename.png`

**Python dependencies** are in `requirements.txt`. The project was originally developed with Python 3.8 but should work with modern Python versions.

**Deployment** uses `ghp-import` to push the generated site to GitHub Pages. The Makefile pushes the `gh-pages` branch to `main`.
