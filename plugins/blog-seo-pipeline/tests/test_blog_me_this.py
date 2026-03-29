from __future__ import annotations

import json
from pathlib import Path


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "peddigrohr-anfaenger-guide"


def test_parse_seed_target_supports_latest_keyword_request():
    from scripts.blog_me_this import parse_seed_target

    target = parse_seed_target("blog me this latest keyword from retool")

    assert target == {"type": "external_latest_keyword", "value": "latest_keyword"}


def test_parse_seed_target_supports_local_directory():
    from scripts.blog_me_this import parse_seed_target

    target = parse_seed_target(f"blog me this {FIXTURE_DIR}")

    assert target == {"type": "local_path", "value": str(FIXTURE_DIR)}


def test_run_writes_plugin_outputs(tmp_path: Path):
    from scripts.blog_me_this import run

    job_dir = tmp_path / FIXTURE_DIR.name
    job_dir.mkdir()
    for source in FIXTURE_DIR.iterdir():
        job_dir.joinpath(source.name).write_bytes(source.read_bytes())

    result = run(f"blog me this {job_dir}")

    assert result["mode"] == "qa-article"
    assert result["family"] == "deep-dive-guide"
    assert result["job_dir"] == str(job_dir)
    assert result["proposal_count"] >= 1
    assert (job_dir / "qa-report.plugin.md").exists()
    assert (job_dir / "revision-plan.plugin.md").exists()
    proposals = json.loads((job_dir / "template-proposals.plugin.json").read_text(encoding="utf-8"))
    assert proposals[0]["target"]


def test_run_revise_mode_writes_revised_article(tmp_path: Path):
    from scripts.blog_me_this import run

    job_dir = tmp_path / FIXTURE_DIR.name
    job_dir.mkdir()
    for source in FIXTURE_DIR.iterdir():
        if source.name == "article.html":
            content = source.read_text(encoding="utf-8").replace("<h2>FAQ</h2>\n<p>Wie lange einweichen? Bis das Material biegsam ist.</p>", "")
            job_dir.joinpath(source.name).write_text(content, encoding="utf-8")
        else:
            job_dir.joinpath(source.name).write_bytes(source.read_bytes())

    result = run(f"revise article {job_dir}")

    assert result["mode"] == "revise-article"
    assert result["revised_path"].endswith("article-revised.plugin.html")
    assert (job_dir / "article-revised.plugin.html").exists()
