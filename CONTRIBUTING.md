# Contributing to Mycel Agent SDK

Thank you for your interest in improving this project. This repository uses a
**maintainer-only `main` branch**: direct pushes to `main` are restricted to
designated maintainers. Everyone else contributes through **feature branches**
and **pull requests**.

## Before you start

1. Read this document and the **[Code of Conduct](CODE_OF_CONDUCT.md)**.
2. Skim **[AGENTS.md](AGENTS.md)** for repo structure, testing commands, and
   policies for substantive code changes.
3. For larger work, consider the **[ExecPlan](PLANS.md)** guidance in `AGENTS.md`.

## Who can push what

| Role | Push to `main` | Feature branches |
| ---- | -------------- | ---------------- |
| **Maintainers** (e.g. org owners listed in branch protection) | Yes | Yes |
| **Collaborators with write access** | No (blocked by branch protection) | Yes |
| **Community members without repo write** | Depends on org policy — forks may be disabled; ask for collaborator access to open PRs from a branch on this repo | N/A without access |

If you are unsure whether you have the right access, open an **issue** first
or contact **[info@mycel-ai.de](mailto:info@mycel-ai.de)**.

## Workflow (required)

1. **Do not commit directly to `main`.** Create a branch from the latest `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/short-description
   ```
2. **Make focused changes** with clear commits (imperative messages, small
   logical units when possible).
3. **Run checks** before opening a PR (see `AGENTS.md` — typically `make format`,
   `make lint`, `make typecheck`, `make tests` when runtime tests or build
   config change).
4. **Open a pull request** into `main`. Describe motivation, approach, and any
   breaking or user-visible behavior.
5. **Respond to review feedback.** A maintainer will merge when the PR is ready.

## Pull request expectations

- Prefer **one PR per feature or fix**; avoid unrelated drive-by changes.
- Link related issues when applicable.
- Update **docs** and **tests** when behavior or public APIs change.
- Avoid committing **secrets**, `.env` files, or credentials.

## Reporting issues

- Use **GitHub Issues** for bugs and feature discussions.
- For security-sensitive reports, contact the maintainers privately (see
  `SECURITY.md` if present, or email **info@mycel-ai.de**).

## License

By contributing, you agree that your contributions will be licensed under the
same terms as the project — see **[LICENSE](LICENSE)** and **[NOTICE](NOTICE)**.
