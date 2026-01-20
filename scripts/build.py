#!/usr/bin/env python3

import os
import subprocess
import argparse
import shutil
import json
from typing import List, Dict, Any
from pathlib import Path


# Academic site files to copy (relative to repo root)
ACADEMIC_SITE_FILES = [
    "index.html",
    "cv.html",
    "research.html",
    "publications.html",
    "favicon.svg",
    ".nojekyll",
]

ACADEMIC_SITE_DIRS = [
    "css",
    "js",
    "images",
    "data",
]


def copy_academic_site(output_dir: str) -> None:
    """Copy academic site files to output directory."""
    print("Copying academic site files...")

    os.makedirs(output_dir, exist_ok=True)

    # Copy individual files
    for filename in ACADEMIC_SITE_FILES:
        src = Path(filename)
        if src.exists():
            dst = Path(output_dir) / filename
            shutil.copy2(src, dst)
            print(f"  Copied {filename}")

    # Copy directories
    for dirname in ACADEMIC_SITE_DIRS:
        src = Path(dirname)
        if src.exists():
            dst = Path(output_dir) / dirname
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  Copied {dirname}/")


def export_html_wasm(notebook_path: str, output_dir: str, as_app: bool = False) -> bool:
    """Export a single marimo notebook to HTML format.

    Returns:
        bool: True if export succeeded, False otherwise
    """
    output_path = notebook_path.replace(".py", ".html")

    cmd = ["marimo", "export", "html-wasm"]
    if as_app:
        print(f"Exporting {notebook_path} to {output_path} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])
    else:
        print(f"Exporting {notebook_path} to {output_path} as notebook")
        cmd.extend(["--mode", "edit"])

    try:
        output_file = os.path.join(output_dir, output_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd.extend([notebook_path, "-o", output_file])
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error exporting {notebook_path}:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error exporting {notebook_path}: {e}")
        return False


def load_teaching_config() -> Dict[str, Any]:
    """Load teaching configuration from JSON file."""
    config_path = Path("teaching_config.json")
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {"courses": []}


def generate_teaching_page(all_notebooks: List[str], output_dir: str) -> None:
    """Generate the teaching.html page with notebook links grouped by course."""
    print("Generating teaching.html")

    config = load_teaching_config()
    teaching_path = os.path.join(output_dir, "teaching.html")

    # Build a set of all configured notebooks
    configured_notebooks = set()
    for course in config.get("courses", []):
        configured_notebooks.update(course.get("notebooks", []))

    # Find unconfigured notebooks
    unconfigured = [nb for nb in all_notebooks if nb not in configured_notebooks]

    def make_card(notebook: str) -> str:
        notebook_name = notebook.split("/")[-1].replace(".py", "")
        display_name = notebook_name.replace("_", " ").replace("-", " ").title()
        html_path = notebook.replace(".py", ".html")
        return f'''                <a href="{html_path}" class="notebook-card">
                    <span class="notebook-name">{display_name}</span>
                    <span class="notebook-arrow">&#8594;</span>
                </a>'''

    def make_external_card(notebook: Dict[str, str]) -> str:
        """Generate HTML card for an external molab notebook."""
        display_name = notebook.get("name", "Notebook")
        url = notebook.get("url", "#")
        return f'''                <a href="{url}" class="notebook-card external-notebook" target="_blank" rel="noopener noreferrer">
                    <span class="notebook-name">{display_name}</span>
                    <span class="notebook-arrow">&#8599;</span>
                </a>'''

    def make_section(title: str, code: str | None, notebooks: List[str], external_notebooks: List[Dict[str, str]] | None = None) -> str:
        """Generate HTML for a course section."""
        # Filter to only existing local notebooks
        existing = [nb for nb in notebooks if nb in all_notebooks]
        external = external_notebooks or []

        if not existing and not external:
            return ""

        header = f"{title} ({code})" if code else title
        section_id = code.lower() if code else title.lower().replace(" ", "-")
        cards = "\n".join(make_card(nb) for nb in existing)
        external_cards = "\n".join(make_external_card(nb) for nb in external)
        all_cards = "\n".join(filter(None, [cards, external_cards]))

        return f'''
            <section class="notebook-section" id="{section_id}">
                <h2>{header}</h2>
                <div class="notebook-grid">
{all_cards}
                </div>
                <a href="#top" class="back-to-top">&uarr; Top</a>
            </section>
'''

    try:
        with open(teaching_path, "w") as f:
            f.write(
                """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Interactive teaching materials - marimo notebooks by Prof. Dr. Christoph M. Flath">
    <title>Teaching Materials | Christoph M. Flath</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Crimson+Pro:ital,wght@0,400;0,500;0,600;1,400&family=Caveat:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
    <style>
        .teaching-intro {
            margin-bottom: var(--spacing-xl);
        }
        .teaching-intro p {
            font-size: 1.1rem;
            color: var(--text-light);
        }
        .marimo-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: var(--spacing-md);
        }
        .marimo-badge img {
            height: 24px;
        }
        .marimo-badge a {
            border-bottom: none;
        }
        .marimo-badge a:hover {
            border-bottom: none;
        }
        .notebook-section {
            margin-bottom: var(--spacing-xl);
        }
        .notebook-section h2 {
            font-family: var(--font-accent);
            font-size: 1.6rem;
            color: var(--primary-color);
            margin-bottom: var(--spacing-lg);
            position: relative;
            display: inline-block;
        }
        .notebook-section h2::after {
            content: '';
            position: absolute;
            bottom: -6px;
            left: 0;
            width: 100%;
            height: 2px;
            background: var(--pencil-gray);
            mask-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 4' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 2 Q10 0, 20 2 T40 2 T60 2 T80 2 T100 2' stroke='black' fill='none' stroke-width='3'/%3E%3C/svg%3E");
            -webkit-mask-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 4' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 2 Q10 0, 20 2 T40 2 T60 2 T80 2 T100 2' stroke='black' fill='none' stroke-width='3'/%3E%3C/svg%3E");
        }
        .notebook-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: var(--spacing-md);
        }
        .notebook-card {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-md) var(--spacing-lg);
            height: 60px;
            background: linear-gradient(135deg, var(--card-gradient-start) 0%, var(--card-gradient-end) 100%);
            border: 2px solid var(--pencil-gray);
            border-radius: 3px 5px 4px 6px;
            box-shadow:
                2px 2px 0 var(--border-color),
                3px 3px 6px rgba(0,0,0,0.06);
        }
        .notebook-card:nth-child(1) { transform: rotate(-0.6deg); }
        .notebook-card:nth-child(2) { transform: rotate(0.8deg); }
        .notebook-card:nth-child(3) { transform: rotate(0.4deg); }
        .notebook-card:nth-child(4) { transform: rotate(-0.5deg); }
        .notebook-card:nth-child(5) { transform: rotate(0.7deg); }
        .notebook-card:nth-child(6) { transform: rotate(-0.4deg); }
        .notebook-name {
            font-family: var(--font-main);
            font-weight: 500;
            color: var(--text-color);
            line-height: 1.3;
        }
        .notebook-card:hover .notebook-name {
            color: var(--primary-color);
        }
        .notebook-arrow {
            color: var(--primary-color);
            font-size: 1.2rem;
        }
        .external-notebook {
            border-style: dashed;
        }
        .external-notebook .notebook-arrow {
            font-size: 1rem;
        }
        /* Course navigation links */
        .course-nav {
            margin-bottom: var(--spacing-xl);
        }
        .course-nav-level {
            margin-bottom: var(--spacing-md);
        }
        .course-nav-level h3 {
            font-family: var(--font-accent);
            font-size: 1.1rem;
            color: var(--text-light);
            margin-bottom: var(--spacing-sm);
        }
        .course-nav-links {
            display: flex;
            flex-wrap: wrap;
            gap: var(--spacing-sm);
        }
        .course-nav-link {
            font-family: var(--font-accent);
            font-size: 1.1rem;
            color: var(--text-color);
            padding: var(--spacing-sm) var(--spacing-md);
            background: linear-gradient(135deg, var(--card-gradient-start) 0%, var(--card-gradient-end) 100%);
            border: 2px solid var(--pencil-gray);
            box-shadow: 2px 2px 0 var(--border-color);
            border-radius: 3px 5px 4px 6px;
            text-decoration: none;
        }
        .course-nav-link:nth-child(1) { transform: rotate(-0.5deg); }
        .course-nav-link:nth-child(2) { transform: rotate(0.7deg); }
        .course-nav-link:nth-child(3) { transform: rotate(-0.4deg); }
        .course-nav-link:nth-child(4) { transform: rotate(0.6deg); }
        .course-nav-link:hover {
            color: var(--primary-color);
        }
        .back-to-top {
            display: block;
            text-align: right;
            margin-top: var(--spacing-md);
            font-family: var(--font-accent);
            font-size: 0.9rem;
            color: var(--text-light);
            border-bottom: none;
        }
        .back-to-top:hover {
            color: var(--primary-color);
        }
        .level-header {
            font-family: var(--font-accent);
            font-size: 1.3rem;
            color: var(--text-light);
            margin: var(--spacing-xl) 0 var(--spacing-md) 0;
            padding-bottom: var(--spacing-sm);
            border-bottom: 1px solid var(--border-color);
        }
        .level-header:first-of-type {
            margin-top: 0;
        }
        @media (max-width: 768px) {
            .course-nav-link {
                font-family: var(--font-main);
                font-size: 0.9rem;
                transform: none;
                border-radius: 4px;
                box-shadow: none;
                border: 1px solid var(--border-color);
                background: var(--background);
            }
        }
        @media (max-width: 768px) {
            .notebook-card {
                transform: none;
                border-radius: 4px;
                box-shadow: none;
                border: 1px solid var(--border-color);
                background: var(--background);
            }
        }
        .page-content {
            padding: var(--spacing-xl) 0;
        }
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to content</a>
    <!-- Header -->
    <header class="site-header">
        <div class="container">
            <a href="index.html" class="site-title">Christoph M. Flath</a>
            <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">&#9776;</button>
            <div class="header-right">
                <nav class="main-nav">
                    <a href="index.html">Home</a>
                    <a href="publications.html">Publications</a>
                    <a href="research.html">Research Areas</a>
                    <a href="teaching.html" class="active">Teaching</a>
                    <a href="cv.html">CV</a>
                </nav>
                <button class="theme-toggle" aria-label="Toggle dark mode">
                    <span class="icon-moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></span>
                    <span class="icon-sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></span>
                </button>
            </div>
        </div>
    </header>

    <main class="page-content" id="main-content">
        <div class="container">
            <h1 id="top">Interactive Teaching Materials</h1>

            <div class="teaching-intro">
                <p>
                    These interactive notebooks are built with marimo, a reactive Python notebook environment.
                    They run entirely in your browser using WebAssembly - no installation required.
                    Feel free to explore, modify, and experiment with the code.
                </p>
                <div class="marimo-badge">
                    <span>Powered by</span>
                    <a href="https://marimo.io" target="_blank" rel="noopener noreferrer">
                        <img src="https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/marimo-logotype-thick.svg" alt="marimo">
                    </a>
                </div>
            </div>
"""
            )

            # Group courses by level
            courses = config.get("courses", [])
            bachelor_courses = [c for c in courses if c.get("level") == "bachelor"]
            master_courses = [c for c in courses if c.get("level") == "master"]

            # Helper to check if course has content
            def course_has_content(course: Dict[str, Any]) -> bool:
                local_nbs = [nb for nb in course.get("notebooks", []) if nb in all_notebooks]
                external_nbs = course.get("external_notebooks", [])
                return bool(local_nbs or external_nbs)

            # Generate navigation
            nav_html = '''
            <nav class="course-nav">
                <div class="course-nav-level">
                    <h3>Bachelor</h3>
                    <div class="course-nav-links">
'''
            for course in bachelor_courses:
                if course_has_content(course):
                    code = course.get("code", "")
                    section_id = code.lower() if code else course.get("name", "").lower().replace(" ", "-")
                    nav_html += f'                        <a href="#{section_id}" class="course-nav-link">{course.get("name", "")}</a>\n'
            nav_html += '''                    </div>
                </div>
                <div class="course-nav-level">
                    <h3>Master</h3>
                    <div class="course-nav-links">
'''
            for course in master_courses:
                if course_has_content(course):
                    code = course.get("code", "")
                    section_id = code.lower() if code else course.get("name", "").lower().replace(" ", "-")
                    nav_html += f'                        <a href="#{section_id}" class="course-nav-link">{course.get("name", "")}</a>\n'
            nav_html += '''                    </div>
                </div>
            </nav>
'''
            f.write(nav_html)

            # Generate Bachelor sections
            f.write('            <h3 class="level-header">Bachelor Courses</h3>\n')
            for course in bachelor_courses:
                section_html = make_section(
                    course.get("name", "Untitled"),
                    course.get("code"),
                    course.get("notebooks", []),
                    course.get("external_notebooks", [])
                )
                if section_html:
                    f.write(section_html)

            # Generate Master sections
            f.write('            <h3 class="level-header">Master Courses</h3>\n')
            for course in master_courses:
                section_html = make_section(
                    course.get("name", "Untitled"),
                    course.get("code"),
                    course.get("notebooks", []),
                    course.get("external_notebooks", [])
                )
                if section_html:
                    f.write(section_html)

            # Unconfigured notebooks are intentionally hidden

            f.write(
                """
        </div>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="container">
            <p>&copy; <span id="copyright-year">2026</span> Christoph M. Flath</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>"""
            )
        print(f"  Generated {teaching_path}")
    except IOError as e:
        print(f"Error generating teaching.html: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build academic site with marimo notebooks")
    parser.add_argument(
        "--output-dir", default="_site", help="Output directory for built files"
    )
    args = parser.parse_args()

    # Step 1: Copy academic site files
    copy_academic_site(args.output_dir)

    # Step 2: Find all notebooks
    all_notebooks: List[str] = []
    for directory in ["notebooks", "apps"]:
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Warning: Directory not found: {dir_path}")
            continue

        # Only get .py files directly in the directory, not in subdirs like __marimo__
        for path in dir_path.glob("*.py"):
            all_notebooks.append(str(path))

    if not all_notebooks:
        print("No notebooks found!")
        return

    print(f"\nFound {len(all_notebooks)} notebooks to export")

    # Step 3: Export notebooks sequentially
    for nb in all_notebooks:
        export_html_wasm(nb, args.output_dir, as_app=nb.startswith("apps/"))

    # Step 4: Generate teaching page
    generate_teaching_page(all_notebooks, args.output_dir)

    print(f"\nBuild complete! Output in {args.output_dir}/")


if __name__ == "__main__":
    main()
