# GitHub Copilot Instructions for mist_openapi Project

## Project Structure
- **Source of Truth**: `workdir/openapi.yaml` is the primary file
- **Generated Files**: Root-level files are auto-generated from `workdir/openapi.yaml`:
  - `mist.openapi.json`
  - `mist.openapi.yaml`
  - `mist.postman.json`
  - `mist.postman.v2.json`
  - `mist.postman_env.json`
- **Generation Script**: `workdir/generate.sh` (and related Python scripts) creates all generated files

## PR Review Guidelines

### OpenAPI File Changes (`workdir/openapi.yaml`)
When reviewing changes to `workdir/openapi.yaml`:
1. ✅ Verify `info.version` field has been updated with new version
2. ✅ Verify `info.description` field has been updated with new release date and version information
3. ✅ Check that generated files are present and correctly updated
4. ✅ Confirm `CHANGELOG.md` has an entry for the new OpenAPI version
5. ✅ Validate OpenAPI schema syntax and structure
6. ✅ Ensure backward compatibility or document breaking changes

### Commit Review Strategy
- Focus comments on `workdir/openapi.yaml` changes
- Do NOT repeat the same comment across generated files
- Only flag generated files if they're missing or incorrectly generated

### Schema Quality Checks
- ✅ Endpoint paths follow RESTful conventions
- ✅ Request/response schemas are well-defined
- ✅ Required fields are clearly marked
- ✅ Examples are provided for complex schemas
- ✅ Descriptions are clear and accurate
- 🔐 No sensitive data in examples or defaults (it's possible to see fake API Token, MAC Addresses, username, ... in the descriptions and examples)

### Version Management
- 🔁 Breaking changes must be documented in CHANGELOG.md
- 🔁 Deprecated endpoints/fields should be marked before removal
- 📦 Version numbers follow semantic versioning

### Code Quality
- 🧪 Changes should be validated against OpenAPI specification
- 📉 Avoid duplicate schema definitions
- 🛠 Ensure changes work in both staging and production environments