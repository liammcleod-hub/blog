from __future__ import annotations

import json
import pathlib
import time


def write_orchestrate_files(bundle: dict, out_dir: pathlib.Path, base_dir: pathlib.Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    report_path = out_dir / f"orchestrate_report_{ts}.md"
    approval_path = out_dir / f"orchestrate_approval_{ts}.json"
    sorted_md_path = out_dir / f"orchestrate_sorted_{ts}.md"
    sorted_json_path = out_dir / f"orchestrate_sorted_{ts}.json"
    observe_path = out_dir / f"observe_{ts}.json"
    proposals_json_path = out_dir / f"orchestrate_proposals_{ts}.json"
    proposals_md_path = out_dir / f"orchestrate_proposals_{ts}.md"

    def fmt_row(r: dict) -> str:
        kind = r["kind"]
        cnt = r.get("productsCount", 0)
        curated = " curated" if r.get("curated") else ""
        never = " never-touch" if r.get("never_touch") else ""
        ver = r.get("verification") or {}
        if ver:
            status = "PASS" if ver.get("passed") else "FAIL"
            ratio = ver.get("outlier_ratio")
            coverage = ver.get("coverage_ratio")
            rule_metrics = ver.get("rule_metrics") if isinstance(ver.get("rule_metrics"), dict) else {}
            rule_breadth = rule_metrics.get("rule_count", 0) if kind == "SMART" else 0
            applied_disj = rule_metrics.get("appliedDisjunctively") if kind == "SMART" else None
            disj_str = f" disj={applied_disj}" if kind == "SMART" and applied_disj is not None else ""
            manual_inf = r.get("manual_rule_inference") if isinstance(r.get("manual_rule_inference"), dict) else {}
            manual_breadth_80 = manual_inf.get("rule_breadth_estimate_80") if kind == "MANUAL" else None
            manual_str = f" manual_rule_breadth_80={manual_breadth_80}" if kind == "MANUAL" and manual_breadth_80 is not None else ""
            return (
                f"- [{r['priority']}] {r['title']} (`{r['handle']}`) [{kind}{curated}{never}]"
                f" products={cnt} verify={status} outlier_ratio={ratio} coverage={coverage} rule_breadth={rule_breadth}{disj_str}{manual_str}"
            )
        return f"- [{r['priority']}] {r['title']} (`{r['handle']}`) [{kind}{curated}{never}] products={cnt}"

    def is_airtight(r: dict) -> bool:
        ver = r.get("verification")
        if not isinstance(ver, dict):
            return False
        try:
            return float(ver.get("outlier_ratio") or 0.0) == 0.0
        except Exception:
            return False

    all_rows = list(bundle.get("rows") or [])
    airtight_rows = [r for r in all_rows if is_airtight(r)]
    airtight_handles = {r.get("handle") for r in airtight_rows if r.get("handle")}
    not_airtight_rows = [r for r in all_rows if (r.get("handle") not in airtight_handles)]

    lines: list[str] = []
    lines.append("# Collections Orchestrate Report (MAIN menu only)")
    lines.append("")
    lines.append("## Next Step (Approval Gate)")
    lines.append(f"Edit and mark approved items in: `{approval_path}`")
    lines.append("Mark approval by setting either:")
    lines.append('- `"approve": "X"` (recommended), or')
    lines.append('- `"approved": true`')
    lines.append("Then run:")
    lines.append(f"`python {base_dir / 'collections_cleanup_runner.py'} orchestrate --mode apply --approval-file {approval_path} --yes`")
    lines.append("")

    for prio in ("High", "Mid", "Low"):
        lines.append(f"## {prio} Priority")
        for r in bundle["by_priority"][prio]:
            if r.get("handle") in airtight_handles:
                continue
            lines.append(fmt_row(r))
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    approval_path.write_text(json.dumps({"generated_at": ts, "items": bundle["approvals"]}, ensure_ascii=False, indent=2), encoding="utf-8")

    sorted_lines: list[str] = []
    sorted_lines.append("# Collections Sorted (airtight vs not airtight) — MAIN menu only")
    sorted_lines.append("")
    sorted_lines.append(f"- Airtight (outlier_ratio = 0): {len(airtight_rows)}")
    sorted_lines.append(f"- Not airtight: {len(not_airtight_rows)}")
    sorted_lines.append("")

    def emit_group(header: str, rows: list[dict]) -> None:
        sorted_lines.append(f"## {header}")
        for prio in ("High", "Mid", "Low"):
            sorted_lines.append(f"### {prio}")
            for r in sorted([x for x in rows if x.get("priority") == prio], key=lambda x: (x.get("title") or "", x.get("handle") or "")):
                sorted_lines.append(fmt_row(r))
            sorted_lines.append("")
        sorted_lines.append("")

    emit_group("Airtight (outlier_ratio = 0)", airtight_rows)
    emit_group("Not airtight (outlier_ratio > 0)", not_airtight_rows)

    sorted_md_path.write_text("\n".join(sorted_lines).rstrip() + "\n", encoding="utf-8")
    sorted_json_path.write_text(
        json.dumps({"generated_at": ts, "airtight": airtight_rows, "not_airtight": not_airtight_rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    observe_rows: list[dict] = []
    for r in all_rows:
        rs = r.get("ruleSet") if isinstance(r.get("ruleSet"), dict) else None
        rs_rules = (rs or {}).get("rules") if isinstance(rs, dict) else None
        rs_summary = None
        if isinstance(rs, dict):
            rs_summary = {
                "appliedDisjunctively": rs.get("appliedDisjunctively"),
                "rule_count": len(rs_rules) if isinstance(rs_rules, list) else 0,
                "rule_preview": rs_rules[:5] if isinstance(rs_rules, list) else [],
            }
        observe_rows.append(
            {
                "handle": r.get("handle"),
                "title": r.get("title"),
                "collection_id": r.get("collection_id"),
                "kind": r.get("kind"),
                "curated": bool(r.get("curated")),
                "never_touch": bool(r.get("never_touch")),
                "productsCount": r.get("productsCount"),
                "ruleSet_summary": rs_summary,
                "ruleSet": rs,
                "verification": r.get("verification"),
                "manual_rule_inference": r.get("manual_rule_inference"),
            }
        )

    observe_path.write_text(
        json.dumps({"generated_at": ts, "menu_id": bundle.get("menu_id"), "rows": observe_rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    def _recommendation_for_row(r: dict) -> tuple[str, str]:
        if r.get("never_touch"):
            return "NOOP", "never_touch"
        if r.get("curated"):
            return "NOOP", "curated"
        kind = r.get("kind")
        ver = r.get("verification") if isinstance(r.get("verification"), dict) else {}
        passed = ver.get("passed")
        outlier_ratio = ver.get("outlier_ratio")
        exempt = ver.get("exempt_reason")
        if exempt:
            return "NOOP", f"verify_exempt:{exempt}"
        if kind == "SMART":
            if passed is False:
                # Unless propose emitted a concrete action, this remains a human review item.
                return "REVIEW", "smart_failed_verify"
            try:
                if float(outlier_ratio or 0.0) > 0.2:
                    return "REVIEW", "smart_high_outliers"
            except Exception:
                pass
            return "NOOP", "smart_ok"
        if kind == "MANUAL":
            if passed is False:
                return "REVIEW", "manual_failed_verify"
            # Manual in MAIN always needs a human packaging decision (taxonomy vs curated) even if it "passes".
            return "REVIEW", "manual_passed_verify"
        return "REVIEW", "unknown_kind"

    def _next_steps_for_row(r: dict) -> list[str]:
        kind = r.get("kind")
        ver = r.get("verification") if isinstance(r.get("verification"), dict) else {}
        passed = ver.get("passed")
        outlier_ratio = ver.get("outlier_ratio")
        exempt = ver.get("exempt_reason")
        actions = (r.get("proposal") or {}).get("actions") if isinstance(r.get("proposal"), dict) else {}
        manual_inf = r.get("manual_rule_inference") if isinstance(r.get("manual_rule_inference"), dict) else {}
        manual_b80 = manual_inf.get("rule_breadth_estimate_80") if isinstance(manual_inf, dict) else None

        steps: list[str] = []
        if exempt:
            steps.append(f"No-op: verify exempt (`{exempt}`). If this is wrong, remove from `verify_exempt_handles`.")
            return steps

        if kind == "SMART" and passed is False:
            if isinstance(actions, dict) and actions:
                steps.append("Has an auto-proposed SMART fix; review `actions` then approve/apply.")
                return steps
            steps.append("Run `diagnose` for rule noise and outlier examples, then update ruleSet via a manual override or targeted rule change.")
            steps.append("Goal: reduce outlier_ratio without killing coverage; re-run orchestrate propose to confirm improvement.")
            return steps

        if kind == "MANUAL":
            try:
                out0 = float(outlier_ratio or 0.0) == 0.0
            except Exception:
                out0 = False
            if passed is False:
                steps.append("Membership likely doesn't match the collection intent; clean up MANUAL membership first (or re-scope/rename the collection).")
                steps.append("After cleanup, re-run orchestrate propose; only then consider MANUAL->SMART conversion.")
                return steps
            if out0:
                steps.append("Candidate for MANUAL->SMART (outlier_ratio=0.0).")
                steps.append("Pick a SAFE ruleset: prefer 2+ independent signals (TAG+TYPE, TAG+VENDOR, TYPE+VENDOR). Avoid single broad TAG/TITLE rules.")
                steps.append("Encode the chosen ruleSet under `manual_to_smart_overrides.<handle>` in `collections_cleanup_config.json`, then re-run orchestrate propose.")
                steps.append("If still good, approve/apply `replace_with_smart` to swap MANUAL for SMART (approval-gated).")
                if manual_b80 is not None:
                    steps.append(f"Manual breadth hint: manual_rule_breadth_80={manual_b80}.")
                return steps
            steps.append("Manual passed verify but is in MAIN: decide curated vs taxonomy (curation workflow) or define a conversion override explicitly.")
            return steps

        return steps

    proposal_rows: list[dict] = []
    for r in all_rows:
        prop = r.get("proposal") if isinstance(r.get("proposal"), dict) else {}
        actions = prop.get("actions") if isinstance(prop.get("actions"), dict) else {}

        ver = r.get("verification") if isinstance(r.get("verification"), dict) else None
        manual_inf = r.get("manual_rule_inference") if isinstance(r.get("manual_rule_inference"), dict) else None
        manual_breadth_80 = manual_inf.get("rule_breadth_estimate_80") if isinstance(manual_inf, dict) else None
        rec, rec_reason = _recommendation_for_row(r)

        proposal_rows.append(
            {
                "priority": r.get("priority"),
                "recommendation": {"status": rec, "reason": rec_reason},
                "next_steps": _next_steps_for_row(r),
                "handle": r.get("handle"),
                "title": r.get("title"),
                "collection_id": r.get("collection_id"),
                "kind": r.get("kind"),
                "curated": bool(r.get("curated")),
                "never_touch": bool(r.get("never_touch")),
                "productsCount": r.get("productsCount"),
                "verification": ver,
                "manual_rule_breadth_80": manual_breadth_80,
                "dry_run": r.get("proposal_dry_run"),
                "actions": actions,
                "notes": prop.get("notes") or [],
                "proposal": prop,
            }
        )

    proposals_json_path.write_text(
        json.dumps(
            {
                "generated_at": ts,
                "scope": "MAIN menu only",
                "observe_path": str(observe_path),
                "count": len(proposal_rows),
                "items": proposal_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    def fmt_actions(a: dict) -> str:
        keys = sorted([k for k in a.keys() if isinstance(k, str)])
        return ", ".join(keys) if keys else "(none)"

    def fmt_ruleset_rules(rs: dict | None, *, max_rules: int = 3) -> str:
        if not isinstance(rs, dict):
            return ""
        rules = rs.get("rules") or []
        if not isinstance(rules, list) or not rules:
            return ""
        parts: list[str] = []
        for r in rules[:max_rules]:
            if not isinstance(r, dict):
                continue
            col = (r.get("column") or "").upper()
            rel = (r.get("relation") or "").upper()
            cond = r.get("condition")
            if not cond:
                continue
            if rel == "EQUALS":
                parts.append(f"{col}={cond}")
            elif rel == "CONTAINS":
                parts.append(f"{col}~{cond}")
            else:
                parts.append(f"{col} {rel} {cond}")
        more = len(rules) - len(rules[:max_rules])
        if more > 0:
            parts.append(f"+{more} more")
        return "; ".join(parts)

    mdp: list[str] = []
    mdp.append("# Collections Orchestrate Proposals (MAIN menu only)")
    mdp.append("")
    mdp.append("This file is the **recommendation** output of the loop (full spectrum).")
    mdp.append("")
    mdp.append("What you're looking at:")
    mdp.append("- Every MAIN-menu collection appears here with a recommendation status.")
    mdp.append("- `ACTION`: has explicit proposed actions (will show `actions=...` and `rules=[...]` when applicable).")
    mdp.append("- `REVIEW`: no automatic action proposed, but should be reviewed by a human (e.g. MANUAL in MAIN, or failed verify).")
    mdp.append("- `NOOP`: no change recommended right now (e.g. curated/never-touch, exempt verify, or SMART looks OK).")
    mdp.append("")
    mdp.append("What an action means (high-level):")
    mdp.append("- `replace_with_smart`: create a new SMART collection (temp handle), rename the old MANUAL to `-legacy`, promote the SMART to the original handle, and rewrite MAIN menu item resourceIds to point at the new collection (approval-gated; requires `--yes`).")
    mdp.append("- `update_ruleSet`: modify an existing SMART collection's ruleSet (approval-gated; requires `--yes`).")
    mdp.append("")
    mdp.append("How to apply (after review):")
    mdp.append("- Edit the approval file `orchestrate_approval_<ts>.json` and mark approvals (`approve: \"X\"`).")
    mdp.append("- Run `python shopify_api_work/collections_cleanup_runner.py orchestrate --mode apply --approval-file <file> --yes`.")
    mdp.append("")
    mdp.append(f"- Generated at: `{ts}`")
    mdp.append(f"- Observe snapshot: `{observe_path}`")
    with_actions = sum(1 for it in proposal_rows if isinstance(it.get("actions"), dict) and bool(it.get("actions")))
    mdp.append(f"- Collections in scope: {len(proposal_rows)}")
    mdp.append(f"- With proposed actions: {with_actions}")
    mdp.append("")

    action_counts: dict[str, int] = {}
    for it in proposal_rows:
        acts = it.get("actions") or {}
        if isinstance(acts, dict):
            for k in acts.keys():
                if isinstance(k, str):
                    action_counts[k] = action_counts.get(k, 0) + 1
    if action_counts:
        mdp.append("Action breakdown:")
        for k in sorted(action_counts.keys()):
            mdp.append(f"- {k}: {action_counts[k]}")
        mdp.append("")

    by_prio: dict[str, list[dict]] = {"High": [], "Mid": [], "Low": []}
    for it in proposal_rows:
        p = it.get("priority") or "Low"
        by_prio[p].append(it)
    for p in by_prio:
        by_prio[p].sort(key=lambda x: (x.get("title") or "", x.get("handle") or ""))

    for prio in ("High", "Mid", "Low"):
        mdp.append(f"## {prio} Priority")
        if not by_prio[prio]:
            mdp.append("- (none)")
            mdp.append("")
            continue
        for it in by_prio[prio]:
            rec = it.get("recommendation") or {}
            rec_status = rec.get("status")
            rec_reason = rec.get("reason")
            ver = it.get("verification") or {}
            outlier = ver.get("outlier_ratio") if isinstance(ver, dict) else None
            coverage = ver.get("coverage_ratio") if isinstance(ver, dict) else None
            manual_b80 = it.get("manual_rule_breadth_80")
            extras = []
            if outlier is not None:
                extras.append(f"outlier_ratio={outlier}")
            if coverage is not None:
                extras.append(f"coverage={coverage}")
            if manual_b80 is not None and it.get("kind") == "MANUAL":
                extras.append(f"manual_rule_breadth_80={manual_b80}")
            extra_str = (" " + " ".join(extras)) if extras else ""
            notes = it.get("notes") or []
            note_str = f" — {notes[0]}" if notes and isinstance(notes, list) and isinstance(notes[0], str) and notes[0].strip() else ""
            next_steps = it.get("next_steps") or []
            step_str = ""
            if isinstance(next_steps, list) and next_steps and isinstance(next_steps[0], str) and next_steps[0].strip():
                step_str = f" next={next_steps[0]}"
            dry = it.get("dry_run") if isinstance(it.get("dry_run"), dict) else None
            dry_str = ""
            if isinstance(dry, dict) and isinstance(dry.get("members_total"), int) and isinstance(dry.get("members_matched"), int):
                dry_str = f" dry_run={dry.get('members_matched')}/{dry.get('members_total')}"

            # Add a compact, eyeballable summary of the proposed rule changes.
            actions_obj = it.get("actions") or {}
            rules_summary = ""
            if isinstance(actions_obj, dict):
                if "replace_with_smart" in actions_obj and isinstance(actions_obj.get("replace_with_smart"), dict):
                    rs = (actions_obj.get("replace_with_smart") or {}).get("ruleSet")
                    rules_summary = fmt_ruleset_rules(rs)
                    if rules_summary:
                        rules_summary = f" rules=[{rules_summary}]"
                elif "update_ruleSet" in actions_obj and isinstance(actions_obj.get("update_ruleSet"), dict):
                    rs = actions_obj.get("update_ruleSet")
                    rules_summary = fmt_ruleset_rules(rs)
                    if rules_summary:
                        rules_summary = f" rules=[{rules_summary}]"
            mdp.append(
                f"- [{rec_status}:{rec_reason}] {it.get('title')} (`{it.get('handle')}`) [{it.get('kind')}] actions={fmt_actions(it.get('actions') or {})}{rules_summary}{extra_str}{dry_str}{step_str}{note_str}"
            )
        mdp.append("")

    proposals_md_path.write_text("\n".join(mdp).rstrip() + "\n", encoding="utf-8")

    return {
        "report_path": str(report_path),
        "approval_path": str(approval_path),
        "sorted_md_path": str(sorted_md_path),
        "sorted_json_path": str(sorted_json_path),
        "observe_path": str(observe_path),
        "proposals_json_path": str(proposals_json_path),
        "proposals_md_path": str(proposals_md_path),
    }
