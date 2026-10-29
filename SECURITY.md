# Security policy

## Supported versions

Only the latest published version of `@davi-domingues/toolkit` receives fixes.

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private reporting instead: go to the **Security** tab of this repository and choose **Report a vulnerability**.

I aim to acknowledge reports within 7 days. This is a personal project, so there is no formal SLA.

## Scope

The CLI creates symlinks, junctions and file copies under the user's home directory (`~/.kiro`, `~/.claude`, `~/.config/opencode`). Reports about writing outside those targets, overwriting files the toolkit does not own, or unsafe handling of paths are in scope. The skill, rule and prompt contents are plain text instructions for AI agents.
