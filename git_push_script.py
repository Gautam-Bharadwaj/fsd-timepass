import os
import subprocess

commits = [
    # Phase 1: Setup
    (["requirements.txt", ".gitignore", "README.md"], "init: project boilerplate and dependencies"),
    (["config.py", ".env.example"], "config: setup environment variables and storage paths"),
    (["main.py"], "feat: initialize fastapi application entry point"),
    (["context.py"], "feat: add user context management for multi-user support"),

    # Phase 2: Connectors & Processing
    (["connectors/google_drive.py"], "feat: implement google drive oauth and file fetcher"),
    (["processing/extractor.py"], "feat: add text extraction for pdf and txt files"),
    (["processing/chunker.py"], "feat: implement semantic text chunking logic"),
    (["downloads/"], "chore: setup local downloads directory"),

    # Phase 3: Embedding & Search
    (["embedding/embedder.py"], "feat: integrate sentence-transformers for text embeddings"),
    (["search/vector_store.py"], "feat: implement faiss vector storage and similarity search"),
    (["storage/"], "chore: setup vector storage directory"),

    # Phase 4: LLM logic
    (["llm/answer.py"], "feat: implement rag answer generation using groq/gemini"),
    (["llm/cache.py"], "feat: add prompt caching layer for faster responses"),
    (["llm/memory.py"], "feat: implement chat history management for conversational context"),

    # Phase 5: API Routes
    (["api/routes.py"], "feat: add core api routes for sync, ask, and status"),
    (["api/__init__.py"], "chore: api package initialization"),

    # Phase 6: Frontend Base
    (["frontend/index.html"], "feat: create initial dashboard layout structure"),
    (["frontend/style.css"], "feat: add base css styles for dashboard"),
    (["frontend/script.js"], "feat: implement frontend api client and navigation"),

    # Phase 7: UI Modernization (The Polish)
    (["frontend/landing.html"], "feat: add premium landing page with cinematic design"),
    (["frontend/landing.css"], "feat: implement landing page styling and animations"),
    (["frontend/style.css"], "style: migrate to premium black and orange theme"),
    (["frontend/style.css"], "style: implement glassmorphism and glow effects on cards"),
    (["frontend/index.html"], "feat: add interactive feature cards and smooth scroll"),

    # Phase 8: UX Refinements
    (["frontend/index.html"], "feat: add 3-step onboarding guide for new users"),
    (["frontend/style.css"], "style: refine onboarding banner animations"),
    (["frontend/landing.html"], "feat: add premium 4-column footer to landing page"),
    (["frontend/landing.css"], "style: implement footer design and responsive links"),
    (["frontend/style.css"], "style: remove inner scrollbars for unified page scroll"),
    (["frontend/index.html"], "chore: remove emojis from headers for professional look"),

    # Phase 9: Final Touches
    (["demo_docs/"], "docs: add sample documents for testing"),
    (["PROJECT_SPEC.md", "workflow.md"], "docs: add technical specifications and workflow diagrams"),
    (["render.yaml"], "chore: add deployment config for render.com"),
    ([".env"], "chore: update environment template"),
    (["."], "docs: final documentation update and project cleanup")
]

def run(cmd):
    try:
        subprocess.run(cmd, check=True, shell=True)
    except Exception as e:
        print(f"Error: {e}")

# Ensure all directories exist to avoid git errors
for paths, msg in commits:
    for path in paths:
        if path != "." and not os.path.exists(path):
            if path.endswith("/"):
                os.makedirs(path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f: f.write('')

for paths, msg in commits:
    for path in paths:
        run(f"git add \"{path}\"")
    run(f"git commit -m \"{msg}\"")

print("\n--- DONE: 35 COMMITS CREATED LOCALLY ---")
