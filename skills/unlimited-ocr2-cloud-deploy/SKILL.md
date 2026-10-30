---
name: unlimited-ocr2-cloud-deploy
description: Deploy Baidu Unlimited OCR 2 to an NVIDIA Ubuntu cloud GPU over SSH using its pinned custom SGLang wheel, with an authenticated browser workbench, GPU and RAM monitoring, reusable backups and deployment troubleshooting. Use for Unlimited-OCR-2 cloud deployment, migration or safe Web UI upgrades, not generic document transcription.
---

# Unlimited OCR 2 cloud deployment

Turn an authorized SSH target into a verified browser OCR workbench, and retain a reusable local backup. The bundled path was exercised on Ubuntu 22.04 x86_64, RTX A6000 48GB, CUDA 13 and Python 3.11. This is a tested profile, not a minimum hardware specification.

## Route the task

- Installation or migration: read [deployment.md](references/deployment.md).
- Existing service failure or upgrade: read [operations.md](references/operations.md).
- Acceptance and resource interpretation: read [verification.md](references/verification.md).
- Original version/evidence boundaries: read [tested-setup.md](references/tested-setup.md).

Use SSH credentials or keys supplied for this task, preserve host-key verification, and keep passwords out of scripts, commands, Git and public backups. Resolve the target, login user, directory and access mode from the request/current context; inspect read-only state while genuinely missing choices are clarified.

## Deployment workflow

1. Inspect OS/architecture, NVIDIA driver/GPU, RAM, disk, `/dev/shm`, ports and existing services/proxy. The payload's `scripts/preflight.py` is read-only. Automated installation targets a dedicated Ubuntu 22.04 host; adapt integration on shared hosts rather than overwriting other services.
2. Run `python3 scripts/prepare_deployment.py --output PATH` locally and upload the fresh payload to a new target directory. It includes the custom SGLang wheel and local KaTeX assets. Download the pinned weights on the GPU host. Do not copy runtime data or generated credentials into the skill.
3. Install system packages and the isolated, locked Python environment. Verify the wheel checksum. Keep the existing NVIDIA driver; do not substitute stock PyPI SGLang or mix the native Transformers example's dependencies into this service environment.
4. Download and verify the model snapshot, create original test examples, then configure the requested access mode. Public authenticated HTTPS requires authorization for public access, a resolving domain and reachable 80/443. Otherwise use the documented loopback/SSH-tunnel mode.
5. Wait for passive `/ready`, run real single-page, cross-page and 12-page inference, then check markers, known text, truncation, downloads and browser behavior. CPU-only package checks cannot establish that a new GPU deployment works.
6. Save versions, parameters, relevant logs and validation results locally. Report the entry URL, credential-file location, service commands and backup location without echoing passwords. Exclude user documents and secrets from public artifacts.

## Non-obvious integration constraints

- Keep the customized `sglang-0.5.20.dev13+g75b9b06b02` wheel and model snapshot `c14071b549f4fcab10909f3c4acc6a2edb366947` together with provenance/checksums. Upgrade deliberately; do not silently switch to `main` or `latest`.
- Preserve the upstream misspelling `SGLANG_UOCR_EANABLE_DOC_LIMIT`. Both page windows are 10. The bundled A6000 profile uses static memory fraction 0.70 and small CUDA Graph batches.
- The launcher discovers pip CUDA 13 under `nvidia/cu13`, selects matching GCC/G++, and supplies `lib64 -> lib` plus `libcudart.so` links for JIT. Diagnose compiler/path errors before proposing a driver replacement.
- Use passive `/ready`. The original `/health` path can generate a token and contaminate idle measurements; the launcher also disables health generation for future starts.
- Keep model/Web on `127.0.0.1:10000` and `127.0.0.1:7860`. Public access passes through authenticated HTTPS with target-generated credentials.
- Long-document usage can arrive only at the end. Never invent live token counts. GPU/RAM charts are whole-device/whole-host one-second samples, including service preallocation; do not infer minimum hardware from them.

## Existing work and completion

Do not restart Web/model services while a user is processing a document. For Web updates, stage source outside the deployment and use `scripts/safe_restart_web.py --source-dir STAGING_DIR` with the deployment's Python. It blocks new submissions at Caddy/application, drains uploads and queued/running jobs, installs staged files and restarts only Web. A timeout does not authorize interrupting work. Model changes need their own idle maintenance window.

Preserve interrupted task files. The UI can recover a task in its original mode if complete prepared-page cache remains; otherwise re-upload is needed. Completion of recovery does not prove text accuracy.

Complete authorized deployment and the reviewable local backup before asking for any remaining approval. Invoking this skill does not itself authorize public publishing, messages, SSH-key installation or account credential changes. If blocked, preserve progress and report the actual failing command/state; do not add unrelated infrastructure as a workaround.
