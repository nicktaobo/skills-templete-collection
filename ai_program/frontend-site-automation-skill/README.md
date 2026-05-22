# frontend-site-automation

把 PRD / 设计交付包自动落地成 **Next.js + Cloudflare Workers** 网站的标准 Hermes Skill。

默认能力：

```txt
PRD / 设计稿
  ↓
Next.js + TypeScript + Tailwind 项目
  ↓
React 组件化落地
  ↓
SEO / 法律页 / sitemap / robots
  ↓
数据追踪 / 移动端检查
  ↓
Cloudflare Workers 部署
  ↓
部署后验收报告
```

---

## 1. 适合谁用

适合学员做：

- SEO 工具站
- AI 工具站
- 产品型 Landing Page
- 站点矩阵
- 带表单 / API / 数据 / 任务的轻产品站

默认技术栈：

```txt
Next.js
TypeScript
Tailwind CSS
OpenNext Cloudflare Adapter
Cloudflare Workers
Workers Assets
D1 / KV / R2 / Queues（按需）
```

不默认使用：

```txt
Cloudflare Pages
Next.js output: "export"
dangerouslySetInnerHTML
```

---

## 2. 安装方式

把压缩包解压到 Hermes Skills 目录：

```bash
mkdir -p ~/.hermes/skills/software-development/frontend-site-automation
unzip frontend-site-automation-skill.zip
cp -r frontend-site-automation-skill/* ~/.hermes/skills/software-development/frontend-site-automation/
```

确认目录结构：

```bash
ls ~/.hermes/skills/software-development/frontend-site-automation
```

应该看到：

```txt
SKILL.md
README.md
scripts/
templates/
```

重启 Hermes / 新开会话后生效。

---

## 3. 使用前准备

### 3.1 登录 GitHub CLI

```bash
gh auth status
```

如果没登录：

```bash
gh auth login
```

用于：

- 创建 GitHub 仓库
- clone 项目
- commit / push
- 后续连接 Cloudflare Git Integration

---

### 3.2 登录 Cloudflare Wrangler

```bash
wrangler whoami
# 或
npx wrangler whoami
```

如果没登录：

```bash
wrangler login
# 或
npx wrangler login
```

用于：

- 部署 Cloudflare Worker
- 配置 Worker secrets
- 创建 / 绑定 D1、KV、R2、Queues
- 绑定域名 / routes

本地写代码和 `npm run build` 不需要 Cloudflare 登录。  
自动部署、绑定域名、配置 secrets 才需要。

---

## 4. 输入材料

至少准备：

```txt
域名
项目名
PRD 或产品说明
设计交付包目录
GitHub owner
联系邮箱
```

设计交付包建议结构：

```txt
design-handoff/
├── HANDOFF.md
├── PRD.md
├── landing.html
├── *.html
├── *.png
└── assets/
```

---

## 5. 推荐输入模板

复制模板：

```bash
cp ~/.hermes/skills/software-development/frontend-site-automation/templates/site-inputs.yaml.md ./site-inputs.yaml.md
```

填写：

```yaml
domain: example.com
project_name: example
github_owner: your-github-name
workdir: /root/projects/example
design_dir: /absolute/path/to/design-handoff
prd_path: /absolute/path/to/PRD.md
contact_email: hello@example.com
cloudflare_target: workers

analytics:
  plausible_domain:
  ga_id:
  clarity_id:
  ahrefs_analytics_id:
  gsc_verification:

deployment:
  use_cloudflare_git_integration: true
  bind_custom_domain: true
  configure_email_routing: true
```

---

## 6. 对 Agent 怎么说

最短用法：

```txt
使用 frontend-site-automation skill，把这个 PRD + 设计交付包自动做成 Next.js + Cloudflare Workers 网站。
```

推荐完整 Prompt：

```txt
使用 frontend-site-automation skill 自动做站。

输入：
- 域名：example.com
- 项目名：example
- GitHub owner：your-github-name
- 设计交付包：/absolute/path/to/design-handoff
- PRD：/absolute/path/to/PRD.md
- 联系邮箱：hello@example.com

要求：
1. 默认使用 Next.js + TypeScript + Tailwind CSS + OpenNext + Cloudflare Workers。
2. 不要使用 Cloudflare Pages。
3. 不要配置 output: "export"。
4. 不要使用 dangerouslySetInnerHTML。
5. 把设计稿 HTML 按 section 拆成 React 组件。
6. 补齐 /privacy-policy、/terms-of-service、sitemap.ts、robots.ts。
7. 如果提供了追踪 ID，就接入 Plausible / GA4 / Clarity / Ahrefs / GSC。
8. 检查 320 / 375 / 390 / 768 / 1024 移动端宽度。
9. 部署前运行 npm run build 和 npm run preview。
10. 如果 gh auth status 和 wrangler whoami 都通过，就部署到 Cloudflare Workers。
11. 最后输出实施报告。
```

---

## 7. 自动化流程

Skill 会按阶段执行：

```txt
Phase 0  Preflight：检查环境、输入材料、GitHub/Cloudflare 登录状态
Phase 1  Project Init：创建或复用 Next.js + Workers 项目
Phase 2  Design Extraction：读取 PRD 和设计稿，提取页面结构
Phase 3  Component Build：把 HTML 拆成 React 组件
Phase 4  Routes / SEO / Legal：补路由、metadata、法律页、sitemap、robots
Phase 5  Links：替换死链，补交叉导航
Phase 6  Interactions：补 FAQ、菜单、表单、CTA 事件
Phase 7  Analytics：接入追踪平台
Phase 8  Mobile QA：检查移动端和横向溢出
Phase 9  Build / Preview：运行 npm run build + npm run preview
Phase 10 Deploy：部署 Cloudflare Workers
Phase 11 Verify：部署后验收
```

---

## 8. 运行 preflight 检查

进入项目目录后：

```bash
~/.hermes/skills/software-development/frontend-site-automation/scripts/preflight.sh .
```

它会检查：

- 当前路径
- Node / npm / git / wrangler 版本
- Git 状态
- package scripts
- 是否存在 `dangerouslySetInnerHTML`
- 是否误用了 `output: "export"`
- 是否还有 `href="#"`
- 是否缺少 sitemap / robots 等关键文件

---

## 9. 移动端溢出检查

打开浏览器 DevTools Console，粘贴：

```js
// ~/.hermes/skills/software-development/frontend-site-automation/scripts/mobile-overflow-check.js
```

或者直接复制文件内容执行。

检查宽度：

```txt
320px
360px
375px
390px
768px
1024px
```

如果返回 `overflow: true`，说明页面有横向溢出。

---

## 10. 有无 Cloudflare Token 的区别

### 只做本地站点

不需要 Cloudflare token。

可以完成：

```txt
代码生成
组件拆分
SEO / 法律页
数据追踪代码
npm run build
```

### 自动部署上线

需要满足其一：

```bash
wrangler whoami
```

或 CI 环境里有：

```bash
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID
```

学员本机通常用：

```bash
gh auth status
wrangler whoami
```

这两个通过就够。

如果 Cloudflare 未登录，Skill 会停在：

```txt
READY_FOR_DEPLOY
```

并输出手动部署命令。

---

## 11. 交付结果

完成后应输出：

```txt
GitHub 仓库
Cloudflare Worker URL
正式域名
变更文件清单
build / preview 结果
移动端检查结果
SEO 文件检查结果
部署后验收清单
实施报告路径
```

实施报告模板在：

```txt
templates/implementation-report.md
```

默认报告路径：

```txt
deliverables/frontend/implementation-report-YYYYMMDD.md
```

---

## 12. 常见问题

### Q1：为什么不用 Cloudflare Pages？

因为产品型小站后续通常会长出：

```txt
API
表单
登录
额度
数据库
队列
Webhook
Cron
```

这些更适合 Cloudflare Workers。

一句话：

> Pages 是静态站托管，Workers 是产品运行底座。

---

### Q2：为什么不能用 `output: "export"`？

它会把 Next.js 变成纯静态导出，限制：

```txt
Route Handlers
Server Actions
SSR / ISR
动态 API
D1 / KV / R2 / Queues
```

默认不要用。

---

### Q3：为什么不用 `dangerouslySetInnerHTML`？

因为它只是在页面里塞一坨 HTML，不利于：

```txt
交互
埋点
组件复用
状态管理
SEO metadata
后续维护
```

设计稿 HTML 应拆成 React 组件。

---

### Q4：如果没有追踪 ID 怎么办？

可以先留空。Skill 会保留组件结构，不强行接入。

后续拿到 ID 后再配置：

```txt
NEXT_PUBLIC_PLAUSIBLE_DOMAIN
NEXT_PUBLIC_GA_ID
NEXT_PUBLIC_CLARITY_ID
NEXT_PUBLIC_AHREFS_ANALYTICS_ID
```

---

### Q5：如果 `wrangler whoami` 失败怎么办？

运行：

```bash
wrangler login
```

或：

```bash
npx wrangler login
```

登录后再检查：

```bash
wrangler whoami
```

---

## 13. 最小验收标准

```txt
[ ] 首页可访问
[ ] 移动端无横向滚动
[ ] CTA 可点击
[ ] Footer 链接正确
[ ] /privacy-policy 可访问
[ ] /terms-of-service 可访问
[ ] /sitemap.xml 可访问
[ ] /robots.txt 可访问
[ ] npm run build 通过
[ ] npm run preview 通过
[ ] 部署到 Cloudflare Workers 或输出 READY_FOR_DEPLOY
```
