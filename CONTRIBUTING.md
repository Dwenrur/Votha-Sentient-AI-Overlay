# Contributing to Votha Sentient Overlay

Thank you for your interest in contributing!  
Votha Sentient Overlay is an open, experimental research project exploring adaptive AI reasoning.  
We welcome thoughtful code, documentation, and discussion contributions.

---

## 🧾 Legal and Licensing

All contributions fall under the **PolyForm Noncommercial License 1.0.0**.  
By submitting a pull request, you agree to the terms of the **Contributor License Agreement (CLA)** found in [`/CLA.md`](./CLA.md) or [`/Votha_Sentient_Overlay_Contributor_Agreement.pdf`](./Votha_Sentient_Overlay_Contributor_Agreement.pdf).

This ensures:
- You keep ownership of your work.
- The project owner retains the right to use it in commercial contexts.
- The project stays safe from patent disputes (Traditional Patent License included).

Before your first contribution, please:
1. Review the license at [polyformproject.org/licenses/noncommercial/1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0/)
2. Read and sign the CLA https://moccasin-athena-63.tiiny.site
4. Email it to **dwenrur@gmail.com**


---

## 🛠️ Development Workflow

### Branching and Pull Requests
We use a protected `main` branch.  
All changes must come through a **feature branch** and **pull request (PR)**.

1. **Fork** the repository (if external).
2. **Create a new branch** for your feature or fix:
   ```
   git checkout -b feature/my-new-feature

Make your edits and commit with clear messages:
   ```
   git commit -m "Add context module for reasoning layer"
   ```
Pull from main before pushing:
   ```
   git pull origin main
   ```

Push your branch and open a PR:
   ```
   git push origin feature/my-new-feature
   ```

Request review from a maintainer.
One approval is required before merging.


✅ Code Standards

Use clear, modular code with meaningful function names.

Follow PEP 8 (for Python) or project-specific conventions.

Include docstrings/comments for new functions or classes.

Add tests when relevant.

Avoid committing generated or compiled files.

🔍 Commit Messages

Use concise, imperative-style messages:
```
Add reasoning layer to contextual parser
Fix typo in documentation
Refactor dataset loader for clarity
```


🧪 Testing

Before submitting a PR:

Ensure existing tests pass.

Add new tests for your features when possible.

If you can’t test due to environment limits, mark the section with # TODO: needs test.



🔐 Branch Protection Rules (for maintainers)

All PRs require at least 1 review.

All CI/status checks must pass.

No direct pushes to main.

Linear history is enforced (use squash or rebase merges).

Administrators follow the same rules.



💬 Communication

Use GitHub Issues for bug reports and feature requests.

Keep discussions respectful and constructive.

The project thrives on curiosity and clarity — ask before assuming.



🧠 Summary

You may freely contribute, remix, and share under the PolyForm Noncommercial License.
Commercial use requires separate permission.
Every contributor must have a signed CLA on file.

Thank you for helping shape Votha Sentient Overlay!



