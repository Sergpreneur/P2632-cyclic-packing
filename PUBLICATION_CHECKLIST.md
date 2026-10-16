# Before publishing on GitHub

1. Extract this archive and publish the **contents of the enclosing project folder**, preserving `.github/workflows/verify.yml` and subdirectories.
2. Keep `Nefedov Sergey` and `Moscow State University, Mathematics Department` as the author/affiliation unless the author changes them.
3. Run `bash scripts/verify_all.sh` locally or check the GitHub Actions job called `Verify published witness`.
4. Inspect the GitHub Actions job **Build Lean 4 formalization**. Until it succeeds, do *not* say that the Lean sources are compiled or formally checked. If it succeeds, also inspect `#print axioms` before claiming kernel-only verification.
5. Review the manuscript and the literature audit. The displayed result is `12 <= M(31,5,3) <= 13` and the first-discovery priority claim is not established beyond the cited TheoremDB snapshot.
6. Add the eventual repository URL to the paper (optional), README and `CITATION.cff`; no placeholder GitHub URL or DOI is fabricated here.
7. **Choose the license deliberately**: by default no LICENSE file is included, so no reuse grant is implied. The author may choose an open-source code license (e.g. MIT) and a suitable separate license for the manuscript.
8. Publish a tagged release (e.g. `v0.2.0`) only once contents and CI logs are reviewed. A DOI may later be obtained via Zenodo, but none exists in the supplied archive.

## Example CLI upload to a new empty repository

```bash
git init
git add .
git commit -m "Publish twelve-orbit P2632 construction and Lean sources"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

Replace `USERNAME/REPOSITORY` with the actual new GitHub repository address. Alternatively, use GitHub's web interface to upload the extracted project tree, including hidden `.github`.
