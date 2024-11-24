## v0.1.7 (2024-11-24)

### Refactor

- refactor EPUB cover handling and introduce XML utility class

## v0.1.6 (2024-11-22)

### Fix

- update job dependency in build-and-publish workflow
- Merge pull request #18 from Mlara417/fix-release-workflow
- change trigger from pull_request to push in build-and-publish workflow

### Refactor

- rename jobs in workflows for clarity

## v0.1.5 (2024-11-22)

### Fix

- remove unnecessary version input from release job in build-and-publish workflow
- downgrade version from 0.1.5 to 0.1.4 in pyproject.toml
- pass version input to release job in build-and-publish workflow and update release.yml to require version input
- rename create_release job to release in build-and-publish workflow
- add workflow_call trigger to release.yml for improved job invocation
- update build-and-publish workflow to use release.yml and bump version to v0.1.4
- add create_release job to build-and-publish workflow and remove tag push trigger from release workflow
- update release workflow to use correct branch reference and improve changelog generation
- improve release workflow to correctly handle environment variables and enhance logging
- update release workflow to use environment variable for release version and correct changelog command
- update changelog command to use starting revision instead of starting version
- update changelog command to use starting version from latest tag
- use correct syntax for accessing environment variable in release workflow
- set fetch-depth to 0 in checkout step of release workflow
- use environment variable for branch reference in build and publish workflow
- add GitHub CLI setup step and specify commitizen version in release workflow
- add workflow_dispatch input for version release in GitHub Actions
- update release workflow to generate incremental release notes
- add GitHub Actions workflow for automated release creation

### Refactor

- rename job from version_and_release to create-release in release workflow
- rename deployment workflow to build and publish; update version format in pyproject.toml

## v0.1.4 (2024-11-21)

### Fix

- Merge pull request #16 from Mlara417/5-automate-versioning

## v0.1.3 (2024-11-21)

### Fix

- Add deployment workflow for version bump and publishing to Test PyPI
- Update GitHub Actions workflow to use base_ref for checkout reference

## v0.1.2 (2024-11-21)

### Fix

- Update GitHub Actions workflow to include version bump commit and push changes
- Update GitHub Actions workflow for Test PyPI publishing and adjust pyproject.toml configuration
- Update Python version in GitHub Actions workflow to 3.10
- Remove post_bump hook from commitizen configuration in pyproject.toml
- Add version_files to pyproject.toml for version management
- Add tag_format to pyproject.toml for version tagging

## v0.1.0 (2024-11-19)
