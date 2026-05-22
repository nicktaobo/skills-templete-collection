# Frontend Site Automation Inputs

Copy this file to your project note and fill it before running the skill.

```yaml
domain: example.com
project_name: example
github_owner: your-github-name
workdir: /root/projects/example
design_dir: /absolute/path/to/design-handoff
prd_path: /absolute/path/to/PRD.md
contact_email: hello@example.com
cloudflare_target: workers

brand:
  site_name: Example
  language: en
  primary_keyword: example tool
  audience: indie hackers / marketers / developers

analytics:
  plausible_domain:
  plausible_script_url: https://plausible.io/js/script.js
  ga_id:
  clarity_id:
  ahrefs_analytics_id:
  gsc_verification:

seo_pages:
  - slug:
    title:
    description:

features:
  has_tool_form: false
  has_pricing: false
  has_faq: true
  needs_api: false
  needs_d1: false
  needs_kv: false
  needs_r2: false
  needs_queues: false

deployment:
  use_cloudflare_git_integration: true
  bind_custom_domain: true
  configure_email_routing: true
  requires_cloudflare_auth: true
  allow_ready_for_deploy_without_token: true

credentials:
  # Student/local workflow: these two logged-in CLIs are usually enough.
  github_auth_check: gh auth status
  cloudflare_auth_check: wrangler whoami
  # Headless CI / server automation may use env tokens instead.
  cloudflare_api_token_env: CLOUDFLARE_API_TOKEN
  cloudflare_account_id_env: CLOUDFLARE_ACCOUNT_ID
  cloudflare_zone_id_env: CLOUDFLARE_ZONE_ID
```
