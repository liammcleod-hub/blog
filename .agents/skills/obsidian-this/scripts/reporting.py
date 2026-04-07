from __future__ import annotations


def render_init_report(repo: str, proposals: dict) -> str:
    return (
        f"obsidian-this init: configured repo {repo}\n"
        f"- graph roots: {len(proposals['graph_roots'])}\n"
        f"- forbidden roots: {len(proposals['forbidden_roots'])}\n"
        f"- navigation docs: {len(proposals['repo_facing_navigation_docs'])}\n"
        f"- skill note roots: {len(proposals['skill_note_roots'])}\n"
        f"- normalization candidates: {len(proposals['normalization_candidates'])}\n"
        f"- normalization exclusions: {len(proposals['normalization_exclusions'])}"
    )


def render_check_report(repo: str, config: dict, findings: list[dict]) -> str:
    lines = [
        f"obsidian-this check: audited repo {repo}\n"
        f"- graph roots: {len(config['graph_roots'])}\n"
        f"- forbidden roots: {len(config['forbidden_roots'])}\n"
        f"- navigation docs: {len(config['repo_facing_navigation_docs'])}\n"
        f"- findings: {len(findings)}"
    ]
    for finding in findings:
        path = finding.get("path", "<no-path>")
        lines.append(f"- {finding['kind']}: {path}")
    return "\n".join(lines)


def render_fix_report(repo: str, touched: list[str], findings: list[dict]) -> str:
    lines = [
        f"obsidian-this fix: updated repo {repo}",
        f"- touched files: {len(touched)}",
        f"- findings processed: {len(findings)}",
    ]
    for path in touched:
        lines.append(f"- touched: {path}")
    return "\n".join(lines)
