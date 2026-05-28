#!/usr/bin/env python3
"""
Build beautiful static HTML pages for WordSolverX GitHub Pages site.
Each game gets its own unique page with category-specific theming.
"""

import os
import re
import glob
import json

BASE_DIR = "/home/z/my-project/wordsolverx"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PAGES_DIR = os.path.join(BASE_DIR, "pages")

# Game metadata with unique colors, icons, and descriptions
GAME_META = {
    # Solvers
    "wordle-solver": {"name": "Wordle Solver", "icon": "📝", "color": "#6AAA64", "desc": "Solve any Wordle puzzle instantly with our advanced algorithm", "cat": "solver"},
    "quordle-solver": {"name": "Quordle Solver", "icon": "🎯", "color": "#E85D4A", "desc": "Master all 4 Wordle puzzles simultaneously", "cat": "solver"},
    "betweenle-solver": {"name": "Betweenle Solver", "icon": "🔤", "color": "#8B5CF6", "desc": "Find the word between two words alphabetically", "cat": "solver"},
    "colordle-solver": {"name": "Colordle Solver", "icon": "🎨", "color": "#F59E0B", "desc": "Solve daily color puzzles with ease", "cat": "solver"},
    "phoodle-solver": {"name": "Phoodle Solver", "icon": "🍽️", "color": "#EC4899", "desc": "Food-themed Wordle puzzle helper", "cat": "solver"},
    "nerdle-solver": {"name": "Nerdle Solver", "icon": "🔢", "color": "#3B82F6", "desc": "Math equation guessing game solver", "cat": "solver"},
    "waffle-solver": {"name": "Waffle Solver", "icon": "🧇", "color": "#D97706", "desc": "Solve word grid rearrangement puzzles", "cat": "solver"},
    "worldle-solver": {"name": "Worldle Solver", "icon": "🌍", "color": "#10B981", "desc": "Country outline guessing solver", "cat": "solver"},
    "loldle-solver": {"name": "LoLdle Solver", "icon": "⚔️", "color": "#C084FC", "desc": "League of Legends champion guessing solver", "cat": "solver"},
    "narutodle-solver": {"name": "Narutodle Solver", "icon": "🍥", "color": "#FF6B35", "desc": "Naruto character guessing solver", "cat": "solver"},
    "onepiecedle-solver": {"name": "Onepiecedle Solver", "icon": "☠️", "color": "#DC2626", "desc": "One Piece character guessing solver", "cat": "solver"},
    "pokedle-solver": {"name": "Pokedle Solver", "icon": "⚡", "color": "#FACC15", "desc": "Pokemon character guessing solver", "cat": "solver"},
    "dotadle-solver": {"name": "Dotadle Solver", "icon": "🛡️", "color": "#EF4444", "desc": "Dota 2 hero guessing solver", "cat": "solver"},
    "smashdle-solver": {"name": "Smashdle Solver", "icon": "💥", "color": "#7C3AED", "desc": "Super Smash Bros character solver", "cat": "solver"},
    "searchle-solver": {"name": "Searchle Solver", "icon": "🔍", "color": "#4F46E5", "desc": "Search trend guessing solver", "cat": "solver"},
    "spotle-solver": {"name": "Spotle Solver", "icon": "🎵", "color": "#1DB954", "desc": "Spotify music guessing solver", "cat": "solver"},
    "spotle-wordle-solver": {"name": "Spotle Wordle Solver", "icon": "🎶", "color": "#1DB954", "desc": "Spotify Wordle crossover solver", "cat": "solver"},
    "squaredle-solver": {"name": "Squaredle Solver", "icon": "⬛", "color": "#6366F1", "desc": "Board word path solver", "cat": "solver"},
    "hangman-solver": {"name": "Hangman Solver", "icon": "🎪", "color": "#78716C", "desc": "Classic hangman word solver", "cat": "solver"},
    "boggle-solver": {"name": "Boggle Solver", "icon": "🎲", "color": "#059669", "desc": "Boggle grid word finder", "cat": "solver"},
    "kanoodle-solver": {"name": "Kanoodle Solver", "icon": "🧩", "color": "#9333EA", "desc": "Kanoodle puzzle piece solver", "cat": "solver"},
    "minesweeper-solver": {"name": "Minesweeper Solver", "icon": "💣", "color": "#64748B", "desc": "Minesweeper safe move finder", "cat": "solver"},
    "light-out-solver": {"name": "Light Out Solver", "icon": "💡", "color": "#FBBF24", "desc": "Lights out toggle puzzle solver", "cat": "solver"},
    "weaver-solver": {"name": "Weaver Solver", "icon": "🧶", "color": "#A855F7", "desc": "Word ladder transformation solver", "cat": "solver"},
    "word-ladder-solver": {"name": "Word Ladder Solver", "icon": "🪜", "color": "#8B5CF6", "desc": "Word ladder puzzle solver", "cat": "solver"},
    "soundmap-solver": {"name": "Soundmap Solver", "icon": "🗺️", "color": "#06B6D4", "desc": "Music artist guessing solver", "cat": "solver"},
    "canuckle-solver": {"name": "Canuckle Solver", "icon": "🍁", "color": "#DC2626", "desc": "Canadian Wordle puzzle solver", "cat": "solver"},
    "colorfle-solver": {"name": "Colorfle Solver", "icon": "🌈", "color": "#F472B6", "desc": "Color puzzle game solver", "cat": "solver"},
    "countryle-solver": {"name": "Countryle Solver", "icon": "🗺️", "color": "#16A34A", "desc": "Country guessing game solver", "cat": "solver"},
    "dordle-solver": {"name": "Dordle Solver", "icon": "✌️", "color": "#2563EB", "desc": "Double Wordle solver", "cat": "solver"},
    "fibble-solver": {"name": "Fibble Solver", "icon": "🤥", "color": "#F97316", "desc": "Deceptive Wordle variant solver", "cat": "solver"},
    "hardle-solver": {"name": "Hardle Solver", "icon": "💪", "color": "#991B1B", "desc": "Hard mode Wordle solver", "cat": "solver"},
    "octordle-solver": {"name": "Octordle Solver", "icon": "🐙", "color": "#7C3AED", "desc": "8 Wordle puzzles solver", "cat": "solver"},
    "thirdle-solver": {"name": "Thirdle Solver", "icon": "3️⃣", "color": "#0891B2", "desc": "3-letter Wordle solver", "cat": "solver"},
    "warmle-solver": {"name": "Warmle Solver", "icon": "🌡️", "color": "#EF4444", "desc": "Warm/cold Wordle solver", "cat": "solver"},
    "woodle-solver": {"name": "Woodle Solver", "icon": "🪵", "color": "#92400E", "desc": "Wooden-themed Wordle solver", "cat": "solver"},
    "w-peaks-solver": {"name": "W Peaks Solver", "icon": "⛰️", "color": "#475569", "desc": "Word Peaks alphabetical solver", "cat": "solver"},
    "xordle-solver": {"name": "Xordle Solver", "icon": "❎", "color": "#BE185D", "desc": "Dual word Wordle solver", "cat": "solver"},
    "wordle-analyzer": {"name": "Wordle Analyzer", "icon": "📊", "color": "#6366F1", "desc": "Analyze and improve your Wordle strategy", "cat": "solver"},
    "3-letter-wordle-solver": {"name": "3-Letter Wordle Solver", "icon": "3️⃣", "color": "#F59E0B", "desc": "Solver for 3-letter Wordle puzzles", "cat": "solver"},
    "4-letter-wordle-solver": {"name": "4-Letter Wordle Solver", "icon": "4️⃣", "color": "#10B981", "desc": "Solver for 4-letter Wordle puzzles", "cat": "solver"},
    "5-letter-wordle-solver": {"name": "5-Letter Wordle Solver", "icon": "5️⃣", "color": "#6AAA64", "desc": "Solver for 5-letter Wordle puzzles", "cat": "solver"},
    "6-letter-wordle-solver": {"name": "6-Letter Wordle Solver", "icon": "6️⃣", "color": "#3B82F6", "desc": "Solver for 6-letter Wordle puzzles", "cat": "solver"},
    "7-letter-wordle-solver": {"name": "7-Letter Wordle Solver", "icon": "7️⃣", "color": "#8B5CF6", "desc": "Solver for 7-letter Wordle puzzles", "cat": "solver"},
    "8-letter-wordle-solver": {"name": "8-Letter Wordle Solver", "icon": "8️⃣", "color": "#EC4899", "desc": "Solver for 8-letter Wordle puzzles", "cat": "solver"},
    "9-letter-wordle-solver": {"name": "9-Letter Wordle Solver", "icon": "9️⃣", "color": "#EF4444", "desc": "Solver for 9-letter Wordle puzzles", "cat": "solver"},
    "10-letter-wordle-solver": {"name": "10-Letter Wordle Solver", "icon": "🔢", "color": "#F97316", "desc": "Solver for 10-letter Wordle puzzles", "cat": "solver"},
    "11-letter-wordle-solver": {"name": "11-Letter Wordle Solver", "icon": "🔢", "color": "#14B8A6", "desc": "Solver for 11-letter Wordle puzzles", "cat": "solver"},
}

# Daily answers meta
DAILY_GAMES = ["wordle", "quordle", "colordle", "colorfle", "contexto", "semantle", "nerdle",
               "phoodle", "phrazle", "waffle", "worldle", "globle", "searchle", "spotle",
               "loldle", "narutodle", "onepiecedle", "pokedle", "dotadle", "smashdle",
               "betweenle", "canuckle", "countryle", "framed", "worgle"]

ARCHIVE_GAMES = ["wordle-answer", "quordle", "colordle", "colorfle", "contexto", "semantle",
                 "nerdle", "phoodle", "phrazle", "waffle", "worldle", "globle", "searchle",
                 "spotle", "canuckle", "countryle", "framed", "worgle"]

WORDLE_GAMES = ["3-letter", "4-letter", "5-letter", "6-letter", "7-letter", "8-letter",
                "9-letter", "10-letter", "11-letter", "12-letter"]

# Colors per category
CAT_COLORS = {
    "solver": {"primary": "#6AAA64", "gradient": "linear-gradient(135deg, #6AAA64 0%, #4A8A4A 100%)", "bg": "#f0fdf4"},
    "daily": {"primary": "#3B82F6", "gradient": "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)", "bg": "#eff6ff"},
    "archive": {"primary": "#8B5CF6", "gradient": "linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)", "bg": "#f5f3ff"},
    "wordle-game": {"primary": "#F59E0B", "gradient": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)", "bg": "#fffbeb"},
    "info": {"primary": "#64748B", "gradient": "linear-gradient(135deg, #64748B 0%, #475569 100%)", "bg": "#f8fafc"},
}

def md_to_html(md_text):
    """Convert markdown to HTML (simple converter)."""
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    in_faq = False

    for line in lines:
        stripped = line.strip()

        # Skip Page URL line
        if stripped.startswith('**Page URL:**'):
            continue

        # Headings
        if stripped.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            content = stripped[4:]
            html_lines.append(f'<h3>{content}</h3>')
        elif stripped.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            content = stripped[3:]
            html_lines.append(f'<h2>{content}</h2>')
        elif stripped.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            content = stripped[2:]
            html_lines.append(f'<h1>{content}</h1>')
        # List items
        elif stripped.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = stripped[2:]
            # Convert markdown links
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
            # Bold
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            html_lines.append(f'<li>{content}</li>')
        # Empty line
        elif stripped == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
        # Regular paragraph
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            content = stripped
            # Convert markdown links
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
            # Bold
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            html_lines.append(f'<p>{content}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def get_page_meta(filepath, slug):
    """Get metadata for a page based on its path and slug."""
    if slug in GAME_META:
        meta = GAME_META[slug]
        return {**meta, "url": f"https://wordsolverx.com/{slug}"}

    # Daily answer pages
    if "daily-answers" in filepath:
        game_name = slug.replace("-answer-today", "").replace("-", " ").title()
        game_icon_map = {
            "wordle": "📝", "quordle": "🎯", "colordle": "🎨", "colorfle": "🌈",
            "contexto": "🧠", "semantle": "💭", "nerdle": "🔢", "phoodle": "🍽️",
            "phrazle": "💬", "waffle": "🧇", "worldle": "🌍", "globle": "🌎",
            "searchle": "🔍", "spotle": "🎵", "loldle": "⚔️", "narutodle": "🍥",
            "onepiecedle": "☠️", "pokedle": "⚡", "dotadle": "🛡️", "smashdle": "💥",
            "betweenle": "🔤", "canuckle": "🍁", "countryle": "🗺️", "framed": "🎬",
            "worgle": "🔤"
        }
        game_key = slug.replace("-answer-today", "")
        icon = game_icon_map.get(game_key, "🎯")
        color_map = {
            "wordle": "#6AAA64", "quordle": "#E85D4A", "colordle": "#F59E0B",
            "colorfle": "#F472B6", "contexto": "#8B5CF6", "semantle": "#6366F1",
            "nerdle": "#3B82F6", "phoodle": "#EC4899", "phrazle": "#14B8A6",
            "waffle": "#D97706", "worldle": "#10B981", "globle": "#059669",
            "searchle": "#4F46E5", "spotle": "#1DB954", "loldle": "#C084FC",
            "narutodle": "#FF6B35", "onepiecedle": "#DC2626", "pokedle": "#FACC15",
            "dotadle": "#EF4444", "smashdle": "#7C3AED", "betweenle": "#8B5CF6",
            "canuckle": "#DC2626", "countryle": "#16A34A", "framed": "#9333EA",
            "worgle": "#64748B"
        }
        color = color_map.get(game_key, "#3B82F6")
        return {
            "name": f"{game_name} Answer Today",
            "icon": icon,
            "color": color,
            "desc": f"Today's {game_name} answer, hints, and solutions",
            "cat": "daily",
            "url": f"https://wordsolverx.com/{slug}"
        }

    # Archive pages
    if "archives" in filepath:
        game_name = slug.replace("-archive", "").replace("-", " ").title()
        if slug == "wordle-answer-archive":
            game_name = "Wordle"
        return {
            "name": f"{game_name} Archive",
            "icon": "📚",
            "color": "#8B5CF6",
            "desc": f"Complete archive of past {game_name} answers",
            "cat": "archive",
            "url": f"https://wordsolverx.com/{slug}"
        }

    # Wordle game pages
    if "wordle-games" in filepath:
        num = slug.replace("-letter-wordle", "")
        return {
            "name": f"{num}-Letter Wordle",
            "icon": "📝",
            "color": "#F59E0B",
            "desc": f"Play {num}-letter Wordle with solver tools",
            "cat": "wordle-game",
            "url": f"https://wordsolverx.com/{slug}"
        }

    # Info pages
    if "info" in filepath:
        name = slug.replace("-", " ").title()
        return {
            "name": name,
            "icon": "ℹ️",
            "color": "#64748B",
            "desc": name,
            "cat": "info",
            "url": f"https://wordsolverx.com/{slug}"
        }

    # Homepage
    if slug == "homepage":
        return {
            "name": "WordSolverX",
            "icon": "🧩",
            "color": "#6AAA64",
            "desc": "Free Puzzle Solver Tools & Daily Answers",
            "cat": "home",
            "url": "https://wordsolverx.com"
        }

    return {"name": slug.replace("-", " ").title(), "icon": "🎯", "color": "#6AAA64", "desc": "", "cat": "solver", "url": f"https://wordsolverx.com/{slug}"}


def get_related_links(meta, slug):
    """Generate related links for sidebar."""
    links = []

    if meta["cat"] == "solver":
        game_base = slug.replace("-solver", "")
        links.append({"name": f"{game_base.title()} Answer Today", "url": f"https://wordsolverx.com/{game_base}-answer-today", "icon": "📅"})
        links.append({"name": f"{game_base.title()} Archive", "url": f"https://wordsolverx.com/{game_base}-archive", "icon": "📚"})
        links.append({"name": "All Solvers", "url": "https://wordsolverx.com/solver", "icon": "🔧"})
    elif meta["cat"] == "daily":
        game_base = slug.replace("-answer-today", "")
        links.append({"name": f"{game_base.title()} Solver", "url": f"https://wordsolverx.com/{game_base}-solver", "icon": "🔧"})
        links.append({"name": f"{game_base.title()} Archive", "url": f"https://wordsolverx.com/{game_base}-archive", "icon": "📚"})
        links.append({"name": "All Today's Answers", "url": "https://wordsolverx.com/today", "icon": "📅"})
    elif meta["cat"] == "archive":
        game_base = slug.replace("-archive", "")
        links.append({"name": f"{game_base.title()} Answer Today", "url": f"https://wordsolverx.com/{game_base}-answer-today", "icon": "📅"})
        links.append({"name": f"{game_base.title()} Solver", "url": f"https://wordsolverx.com/{game_base}-solver", "icon": "🔧"})
        links.append({"name": "All Archives", "url": "https://wordsolverx.com/archive", "icon": "📚"})

    links.append({"name": "Home", "url": "https://wordsolverx.com", "icon": "🏠"})
    return links


def generate_html(meta, content_html, slug, related_links):
    """Generate a full beautiful HTML page."""
    cat_style = CAT_COLORS.get(meta["cat"], CAT_COLORS["solver"])
    primary = meta.get("color", cat_style["primary"])

    # Breadcrumb
    cat_names = {"solver": "Solvers", "daily": "Daily Answers", "archive": "Archives", "wordle-game": "Wordle Games", "info": "Info", "home": "Home"}

    breadcrumb = f'''
    <nav class="breadcrumb">
        <a href="https://wordsolverx.com">Home</a>
        <span class="sep">›</span>
        <a href="https://wordsolverx.com/{meta["cat"]}">{cat_names.get(meta["cat"], "Pages")}</a>
        <span class="sep">›</span>
        <span class="current">{meta["name"]}</span>
    </nav>'''

    # Related links sidebar
    sidebar_links = ""
    for link in related_links:
        sidebar_links += f'''
        <a href="{link["url"]}" class="sidebar-link">
            <span class="sidebar-icon">{link["icon"]}</span>
            <span>{link["name"]}</span>
        </a>'''

    # CTA button based on category
    if meta["cat"] == "solver":
        cta_url = f"https://wordsolverx.com/{slug}"
        cta_text = "🚀 Try This Solver"
    elif meta["cat"] == "daily":
        cta_url = f"https://wordsolverx.com/{slug}"
        cta_text = "📅 Check Today's Answer"
    elif meta["cat"] == "archive":
        cta_url = f"https://wordsolverx.com/{slug}"
        cta_text = "📚 Browse Archive"
    else:
        cta_url = f"https://wordsolverx.com/{slug}"
        cta_text = "🔗 Visit Page"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta["name"]} - WordSolverX</title>
    <meta name="description" content="{meta['desc']}. Free online tool at WordSolverX.">
    <meta name="keywords" content="{meta['name'].lower()}, {meta['name'].lower()} tool, word solver, puzzle solver, daily answers">
    <link rel="canonical" href="{meta['url']}">
    <meta property="og:title" content="{meta['name']} - WordSolverX">
    <meta property="og:description" content="{meta['desc']}">
    <meta property="og:url" content="{meta['url']}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{meta['name']} - WordSolverX">
    <link rel="icon" href="https://wordsolverx.com/favicon.ico">
    <style>
        :root {{
            --primary: {primary};
            --primary-dark: {primary}dd;
            --primary-light: {primary}22;
            --bg: #ffffff;
            --bg-alt: {cat_style["bg"]};
            --text: #1a1a2e;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --shadow: 0 1px 3px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 40px rgba(0,0,0,0.1);
            --radius: 12px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: var(--text);
            background: var(--bg);
            line-height: 1.7;
        }}

        /* Header */
        .header {{
            background: white;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .header-inner {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--text);
            font-weight: 800;
            font-size: 1.3rem;
        }}

        .logo-icon {{
            width: 36px;
            height: 36px;
            background: var(--primary);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.1rem;
        }}

        .nav-links {{
            display: flex;
            gap: 8px;
        }}

        .nav-links a {{
            text-decoration: none;
            color: var(--text-muted);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .nav-links a:hover {{
            background: var(--primary-light);
            color: var(--primary);
        }}

        /* Hero */
        .hero {{
            background: {cat_style["gradient"]};
            padding: 48px 24px;
            color: white;
        }}

        .hero-inner {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}

        .hero-icon {{
            font-size: 3.5rem;
            margin-bottom: 16px;
            display: block;
        }}

        .hero h1 {{
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 12px;
            line-height: 1.2;
        }}

        .hero p {{
            font-size: 1.15rem;
            opacity: 0.92;
            max-width: 600px;
            margin: 0 auto 24px;
        }}

        .cta-button {{
            display: inline-block;
            background: white;
            color: var(--primary);
            padding: 14px 32px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1rem;
            text-decoration: none;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}

        /* Breadcrumb */
        .breadcrumb {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px 24px;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .breadcrumb a {{
            color: var(--primary);
            text-decoration: none;
        }}

        .breadcrumb .sep {{ margin: 0 6px; }}

        /* Main Layout */
        .main {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px 48px;
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 32px;
        }}

        /* Content */
        .content {{
            min-width: 0;
        }}

        .content h2 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            margin: 32px 0 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--primary-light);
        }}

        .content h3 {{
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--primary-dark);
            margin: 24px 0 12px;
        }}

        .content p {{
            margin: 0 0 16px;
            color: #374151;
        }}

        .content ul {{
            margin: 0 0 16px 24px;
        }}

        .content li {{
            margin: 8px 0;
            color: #374151;
        }}

        .content a {{
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
        }}

        .content a:hover {{
            text-decoration: underline;
        }}

        .content strong {{
            color: var(--text);
        }}

        /* FAQ Section */
        .faq-section {{
            margin-top: 32px;
        }}

        .faq-item {{
            background: var(--bg-alt);
            border-radius: var(--radius);
            margin-bottom: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .faq-question {{
            padding: 16px 20px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text);
        }}

        .faq-question::after {{
            content: '+';
            font-size: 1.3rem;
            color: var(--primary);
            font-weight: 700;
        }}

        .faq-answer {{
            padding: 0 20px 16px;
            color: var(--text-muted);
            display: none;
        }}

        /* Sidebar */
        .sidebar {{
            position: sticky;
            top: 80px;
            align-self: start;
        }}

        .sidebar-card {{
            background: var(--bg-alt);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 20px;
            margin-bottom: 16px;
        }}

        .sidebar-title {{
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        .sidebar-link {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--text);
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.15s;
        }}

        .sidebar-link:hover {{
            background: var(--primary-light);
            color: var(--primary);
        }}

        .sidebar-icon {{
            font-size: 1.1rem;
        }}

        /* Visit Main Site CTA */
        .visit-cta {{
            background: {cat_style["gradient"]};
            border-radius: var(--radius);
            padding: 24px;
            text-align: center;
            color: white;
            margin-top: 16px;
        }}

        .visit-cta p {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 12px;
        }}

        .visit-cta a {{
            display: inline-block;
            background: white;
            color: var(--primary);
            padding: 10px 24px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            font-size: 0.9rem;
        }}

        /* Footer */
        .footer {{
            background: #1a1a2e;
            color: #94a3b8;
            padding: 48px 24px;
        }}

        .footer-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 32px;
        }}

        .footer h4 {{
            color: white;
            margin-bottom: 12px;
            font-size: 0.9rem;
        }}

        .footer a {{
            color: #94a3b8;
            text-decoration: none;
            display: block;
            padding: 3px 0;
            font-size: 0.85rem;
        }}

        .footer a:hover {{ color: white; }}

        .footer-bottom {{
            max-width: 1200px;
            margin: 24px auto 0;
            padding-top: 24px;
            border-top: 1px solid #334155;
            text-align: center;
            font-size: 0.8rem;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .main {{
                grid-template-columns: 1fr;
            }}
            .sidebar {{
                position: static;
            }}
            .hero h1 {{ font-size: 1.6rem; }}
            .hero-icon {{ font-size: 2.5rem; }}
            .nav-links {{ display: none; }}
        }}

        /* Schema markup hidden */
        .schema {{ display: none; }}
    </style>
</head>
<body>

    <!-- Header -->
    <header class="header">
        <div class="header-inner">
            <a href="https://wordsolverx.com" class="logo">
                <div class="logo-icon">🧩</div>
                WordSolverX
            </a>
            <nav class="nav-links">
                <a href="https://wordsolverx.com/solver">Solvers</a>
                <a href="https://wordsolverx.com/today">Daily Answers</a>
                <a href="https://wordsolverx.com/archive">Archives</a>
                <a href="https://wordsolverx.com/guides">Guides</a>
            </nav>
        </div>
    </header>

    <!-- Hero -->
    <section class="hero">
        <div class="hero-inner">
            <span class="hero-icon">{meta["icon"]}</span>
            <h1>{meta["name"]}</h1>
            <p>{meta["desc"]}</p>
            <a href="{cta_url}" class="cta-button">{cta_text}</a>
        </div>
    </section>

    {breadcrumb}

    <!-- Main Content -->
    <main class="main">
        <article class="content">
            {content_html}
        </article>

        <aside class="sidebar">
            <div class="sidebar-card">
                <div class="sidebar-title">Quick Links</div>
                {sidebar_links}
            </div>

            <div class="visit-cta">
                <p>Visit the full interactive tool</p>
                <a href="{meta['url']}">Open on WordSolverX →</a>
            </div>
        </aside>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-inner">
            <div>
                <h4>Solver Tools</h4>
                <a href="https://wordsolverx.com/wordle-solver">Wordle Solver</a>
                <a href="https://wordsolverx.com/quordle-solver">Quordle Solver</a>
                <a href="https://wordsolverx.com/colordle-solver">Colordle Solver</a>
                <a href="https://wordsolverx.com/phoodle-solver">Phoodle Solver</a>
                <a href="https://wordsolverx.com/nerdle-solver">Nerdle Solver</a>
            </div>
            <div>
                <h4>Daily Answers</h4>
                <a href="https://wordsolverx.com/wordle-answer-today">Wordle Today</a>
                <a href="https://wordsolverx.com/quordle-answer-today">Quordle Today</a>
                <a href="https://wordsolverx.com/colordle-answer-today">Colordle Today</a>
                <a href="https://wordsolverx.com/phoodle-answer-today">Phoodle Today</a>
            </div>
            <div>
                <h4>Archives</h4>
                <a href="https://wordsolverx.com/wordle-answer-archive">Wordle Archive</a>
                <a href="https://wordsolverx.com/quordle-archive">Quordle Archive</a>
                <a href="https://wordsolverx.com/archive">All Archives</a>
            </div>
            <div>
                <h4>Company</h4>
                <a href="https://wordsolverx.com/about">About</a>
                <a href="https://wordsolverx.com/contact">Contact</a>
                <a href="https://wordsolverx.com/privacy-policy">Privacy</a>
                <a href="https://wordsolverx.com/terms-of-service">Terms</a>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 WordSolverX. All rights reserved. | <a href="https://wordsolverx.com">wordsolverx.com</a>
        </div>
    </footer>

    <!-- Schema.org structured data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "{meta['name']}",
        "description": "{meta['desc']}",
        "url": "{meta['url']}",
        "isPartOf": {{
            "@type": "WebSite",
            "name": "WordSolverX",
            "url": "https://wordsolverx.com"
        }}
    }}
    </script>
</body>
</html>'''

    return html


def generate_index_html():
    """Generate the main index page with all games organized by category."""

    # Build category sections
    solver_links = ""
    for slug, meta in sorted(GAME_META.items(), key=lambda x: x[1]["name"]):
        solver_links += f'''
        <a href="./{slug}/index.html" class="game-card" style="--card-color: {meta['color']}">
            <div class="game-icon">{meta['icon']}</div>
            <div class="game-name">{meta['name']}</div>
            <div class="game-desc">{meta['desc']}</div>
        </a>'''

    daily_links = ""
    for game in DAILY_GAMES:
        name = game.replace("-", " ").title()
        icon_map = {"wordle": "📝", "quordle": "🎯", "colordle": "🎨", "colorfle": "🌈",
                    "contexto": "🧠", "semantle": "💭", "nerdle": "🔢", "phoodle": "🍽️",
                    "phrazle": "💬", "waffle": "🧇", "worldle": "🌍", "globle": "🌎",
                    "searchle": "🔍", "spotle": "🎵", "loldle": "⚔️", "narutodle": "🍥",
                    "onepiecedle": "☠️", "pokedle": "⚡", "dotadle": "🛡️", "smashdle": "💥",
                    "betweenle": "🔤", "canuckle": "🍁", "countryle": "🗺️", "framed": "🎬",
                    "worgle": "🔤"}
        color_map = {"wordle": "#6AAA64", "quordle": "#E85D4A", "colordle": "#F59E0B",
                    "colorfle": "#F472B6", "contexto": "#8B5CF6", "semantle": "#6366F1",
                    "nerdle": "#3B82F6", "phoodle": "#EC4899", "phrazle": "#14B8A6",
                    "waffle": "#D97706", "worldle": "#10B981", "globle": "#059669",
                    "searchle": "#4F46E5", "spotle": "#1DB954", "loldle": "#C084FC",
                    "narutodle": "#FF6B35", "onepiecedle": "#DC2626", "pokedle": "#FACC15",
                    "dotadle": "#EF4444", "smashdle": "#7C3AED", "betweenle": "#8B5CF6",
                    "canuckle": "#DC2626", "countryle": "#16A34A", "framed": "#9333EA",
                    "worgle": "#64748B"}
        icon = icon_map.get(game, "🎯")
        color = color_map.get(game, "#3B82F6")
        daily_links += f'''
        <a href="./{game}-answer-today/index.html" class="game-card" style="--card-color: {color}">
            <div class="game-icon">{icon}</div>
            <div class="game-name">{name} Answer Today</div>
            <div class="game-desc">Today's {name} solution & hints</div>
        </a>'''

    archive_links = ""
    for game in ARCHIVE_GAMES:
        name = game.replace("-", " ").title()
        if game == "wordle-answer":
            name = "Wordle"
        archive_links += f'''
        <a href="./{game}-archive/index.html" class="game-card" style="--card-color: #8B5CF6">
            <div class="game-icon">📚</div>
            <div class="game-name">{name} Archive</div>
            <div class="game-desc">All past {name} answers</div>
        </a>'''

    wordle_links = ""
    for game in WORDLE_GAMES:
        num = game.split("-")[0]
        colors = {"3": "#F59E0B", "4": "#10B981", "5": "#6AAA64", "6": "#3B82F6",
                  "7": "#8B5CF6", "8": "#EC4899", "9": "#EF4444", "10": "#F97316",
                  "11": "#14B8A6", "12": "#6366F1"}
        color = colors.get(num, "#6AAA64")
        wordle_links += f'''
        <a href="./{game}-wordle/index.html" class="game-card" style="--card-color: {color}">
            <div class="game-icon">{num}️⃣</div>
            <div class="game-name">{num}-Letter Wordle</div>
            <div class="game-desc">Play & solve {num}-letter puzzles</div>
        </a>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordSolverX - Free Puzzle Solver Tools & Daily Answers</title>
    <meta name="description" content="Free online puzzle solvers and daily answers for Wordle, Quordle, Colordle, Phoodle, Nerdle, and 50+ more games.">
    <link rel="canonical" href="https://wordsolverx.com">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1a1a2e;
            background: #f8fafc;
        }}

        .header {{
            background: white;
            border-bottom: 1px solid #e2e8f0;
            padding: 16px 24px;
        }}

        .header-inner {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #1a1a2e;
            font-weight: 800;
            font-size: 1.3rem;
        }}

        .logo-icon {{
            width: 36px; height: 36px;
            background: #6AAA64;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-size: 1.1rem;
        }}

        .hero {{
            background: linear-gradient(135deg, #6AAA64 0%, #3B82F6 50%, #8B5CF6 100%);
            padding: 72px 24px;
            text-align: center;
            color: white;
        }}

        .hero h1 {{
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 16px;
        }}

        .hero p {{
            font-size: 1.25rem;
            opacity: 0.92;
            max-width: 600px;
            margin: 0 auto 32px;
        }}

        .hero-stats {{
            display: flex;
            justify-content: center;
            gap: 48px;
            margin-top: 32px;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-num {{
            font-size: 2rem;
            font-weight: 900;
        }}

        .stat-label {{
            font-size: 0.85rem;
            opacity: 0.8;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }}

        .section {{
            padding: 48px 0;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
        }}

        .section-icon {{
            width: 40px; height: 40px;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem;
        }}

        .section-title {{
            font-size: 1.5rem;
            font-weight: 800;
        }}

        .section-subtitle {{
            color: #64748b;
            font-size: 0.9rem;
        }}

        .game-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 16px;
        }}

        .game-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .game-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-color: var(--card-color);
        }}

        .game-icon {{
            font-size: 2rem;
        }}

        .game-name {{
            font-weight: 700;
            font-size: 0.95rem;
        }}

        .game-desc {{
            font-size: 0.8rem;
            color: #64748b;
            line-height: 1.4;
        }}

        .footer {{
            background: #1a1a2e;
            color: #94a3b8;
            padding: 32px 24px;
            text-align: center;
            font-size: 0.85rem;
        }}

        .footer a {{
            color: #94a3b8;
            text-decoration: none;
        }}

        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2rem; }}
            .hero-stats {{ gap: 24px; }}
            .stat-num {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-inner">
            <a href="https://wordsolverx.com" class="logo">
                <div class="logo-icon">🧩</div>
                WordSolverX
            </a>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>🧩 WordSolverX</h1>
            <p>Free puzzle solver tools and daily answers for 50+ games. Updated every day at midnight.</p>
            <div class="hero-stats">
                <div class="stat">
                    <div class="stat-num">48</div>
                    <div class="stat-label">Solver Tools</div>
                </div>
                <div class="stat">
                    <div class="stat-num">25</div>
                    <div class="stat-label">Daily Answers</div>
                </div>
                <div class="stat">
                    <div class="stat-num">18</div>
                    <div class="stat-label">Archives</div>
                </div>
                <div class="stat">
                    <div class="stat-num">10</div>
                    <div class="stat-label">Wordle Variants</div>
                </div>
            </div>
        </div>
    </section>

    <div class="container">

        <section class="section">
            <div class="section-header">
                <div class="section-icon" style="background: #f0fdf4">🔧</div>
                <div>
                    <div class="section-title">Solver Tools</div>
                    <div class="section-subtitle">Advanced puzzle-solving tools for every game</div>
                </div>
            </div>
            <div class="game-grid">
                {solver_links}
            </div>
        </section>

        <section class="section">
            <div class="section-header">
                <div class="section-icon" style="background: #eff6ff">📅</div>
                <div>
                    <div class="section-title">Daily Answers</div>
                    <div class="section-subtitle">Today's answers updated at midnight</div>
                </div>
            </div>
            <div class="game-grid">
                {daily_links}
            </div>
        </section>

        <section class="section">
            <div class="section-header">
                <div class="section-icon" style="background: #f5f3ff">📚</div>
                <div>
                    <div class="section-title">Answer Archives</div>
                    <div class="section-subtitle">Complete historical records of past solutions</div>
                </div>
            </div>
            <div class="game-grid">
                {archive_links}
            </div>
        </section>

        <section class="section">
            <div class="section-header">
                <div class="section-icon" style="background: #fffbeb">📝</div>
                <div>
                    <div class="section-title">Wordle Variants</div>
                    <div class="section-subtitle">3-letter to 12-letter puzzles</div>
                </div>
            </div>
            <div class="game-grid">
                {wordle_links}
            </div>
        </section>

    </div>

    <footer class="footer">
        &copy; 2026 WordSolverX. All rights reserved. | <a href="https://wordsolverx.com">wordsolverx.com</a>
    </footer>
</body>
</html>'''

    return html


def main():
    # Create docs directory
    os.makedirs(DOCS_DIR, exist_ok=True)

    # Generate index page
    index_html = generate_index_html()
    with open(os.path.join(DOCS_DIR, "index.html"), "w") as f:
        f.write(index_html)
    print("✅ Generated index.html")

    # Process all MD files
    count = 0
    for md_file in glob.glob(os.path.join(PAGES_DIR, "**/*.md"), recursive=True):
        slug = os.path.splitext(os.path.basename(md_file))[0]

        # Skip homepage (use index)
        if slug == "homepage":
            continue

        # Read markdown content
        with open(md_file, "r") as f:
            md_content = f.read()

        # Get page metadata
        meta = get_page_meta(md_file, slug)

        # Convert MD to HTML
        content_html = md_to_html(md_content)

        # Get related links
        related_links = get_related_links(meta, slug)

        # Generate full HTML page
        html = generate_html(meta, content_html, slug, related_links)

        # Create output directory
        out_dir = os.path.join(DOCS_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)

        # Write HTML file
        out_file = os.path.join(out_dir, "index.html")
        with open(out_file, "w") as f:
            f.write(html)

        count += 1
        print(f"✅ {slug}/index.html")

    # Also generate homepage as a separate page
    homepage_md = os.path.join(PAGES_DIR, "homepage.md")
    if os.path.exists(homepage_md):
        with open(homepage_md, "r") as f:
            md_content = f.read()
        meta = get_page_meta(homepage_md, "homepage")
        content_html = md_to_html(md_content)
        related_links = [
            {"name": "All Solvers", "url": "https://wordsolverx.com/solver", "icon": "🔧"},
            {"name": "Daily Answers", "url": "https://wordsolverx.com/today", "icon": "📅"},
            {"name": "Archives", "url": "https://wordsolverx.com/archive", "icon": "📚"},
        ]
        html = generate_html(meta, content_html, "homepage", related_links)
        home_dir = os.path.join(DOCS_DIR, "home")
        os.makedirs(home_dir, exist_ok=True)
        with open(os.path.join(home_dir, "index.html"), "w") as f:
            f.write(html)
        print(f"✅ home/index.html")

    print(f"\n🎉 Generated {count + 1} pages total!")

    # Add .nojekyll to disable Jekyll processing
    with open(os.path.join(DOCS_DIR, ".nojekyll"), "w") as f:
        f.write("")

    # Create CNAME file for custom domain
    with open(os.path.join(DOCS_DIR, "CNAME"), "w") as f:
        f.write("wordsolverx.github.io")

    print("✅ Added .nojekyll and CNAME")


if __name__ == "__main__":
    main()
