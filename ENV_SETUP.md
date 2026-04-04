# 环境变量配置指南

本文档详细说明如何配置 SkillNet 的环境变量。

---

## 📋 目录

- [快速开始](#快速开始)
- [环境变量说明](#环境变量说明)
- [模型选择指南](#模型选择指南)
- [配置示例](#配置示例)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 1. 复制配置模板

```bash
cp .env.example .env
```

### 2. 编辑配置文件

```bash
# 使用您喜欢的编辑器
vim .env
# 或
nano .env
# 或
code .env
```

### 3. 填写必需配置

**最小配置**（仅搜索和下载功能）：
```env
# 无需配置，开箱即用！
```

**基础配置**（创建和评估功能）：
```env
API_KEY=sk-your-openai-api-key-here
SKILLNET_MODEL=gpt-4o
```

**完整配置**（最佳体验）：
```env
API_KEY=sk-your-openai-api-key-here
SKILLNET_MODEL=gpt-4o
GITHUB_TOKEN=ghp-your-github-token-here
GITHUB_MIRROR=https://ghfast.top/
```

---

## 📚 环境变量说明

### OpenAI API 配置

#### `API_KEY` (必需*)

OpenAI API 密钥，用于创建、评估和分析技能。

**获取方式**：
1. 访问 https://platform.openai.com/api-keys
2. 登录您的 OpenAI 账号
3. 点击 "Create new secret key"
4. 复制生成的 API Key

**示例**：
```env
API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901
```

**使用场景**：
- ✅ `skillnet create` - 创建技能
- ✅ `skillnet evaluate` - 评估技能
- ✅ `skillnet analyze` - 分析关系
- ❌ `skillnet search` - 不需要
- ❌ `skillnet download` - 不需要

*注：仅在使用创建、评估、分析功能时必需

---

#### `BASE_URL` (可选)

OpenAI API 的基础 URL，用于配置代理或使用第三方服务。

**默认值**：`https://api.openai.com/v1`

**使用场景**：

1. **使用代理服务**（国内网络）
   ```env
   BASE_URL=https://api.openai-proxy.com/v1
   ```

2. **Azure OpenAI**
   ```env
   BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
   ```

3. **兼容 OpenAI API 的服务**
   ```env
   # DeepSeek
   BASE_URL=https://api.deepseek.com/v1
   
   # 阿里云百炼
   BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   ```

---

#### `SKILLNET_MODEL` (可选)

默认使用的 LLM 模型。

**默认值**：`gpt-4o`

**示例**：
```env
SKILLNET_MODEL=gpt-4o
```

详见 [模型选择指南](#模型选择指南)

---

### GitHub 配置

#### `GITHUB_TOKEN` (强烈推荐)

GitHub Personal Access Token，用于提高 API 速率限制和访问私有仓库。

**获取方式**：
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 设置权限：
   - ✅ `repo` (访问私有仓库)
   - ✅ `public_repo` (仅公开仓库也可)
4. 生成并复制 Token

**示例**：
```env
GITHUB_TOKEN=ghp_abc123def456ghi789jkl012mno345pqr678st
```

**作用**：
- 速率限制：60/小时 → 5000/小时
- 访问私有仓库
- 避免下载时 API 限流

**速率限制对比**：

| 场景 | 无 Token | 有 Token |
|------|---------|----------|
| API 请求限制 | 60/小时 | 5000/小时 |
| 下载大型仓库 | 容易超限 | 正常使用 |
| 批量操作 | 受限 | 流畅 |

---

#### `GITHUB_MIRROR` (国内推荐)

GitHub 镜像地址，用于加速下载。

**推荐镜像**：

| 镜像地址 | 速度 | 稳定性 | 推荐度 |
|---------|------|--------|--------|
| https://ghfast.top/ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🌟 推荐 |
| https://mirror.ghproxy.com/ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 备用 |
| https://github.moeyy.xyz/ | ⭐⭐⭐ | ⭐⭐⭐ | 备用 |

**示例**：
```env
GITHUB_MIRROR=https://ghfast.top/
```

**工作原理**：
```
原始 URL: https://github.com/user/repo
加速后:   https://ghfast.top/https://github.com/user/repo
```

---

### API 服务器配置

#### `HOST` (可选)

Web API 服务器监听地址。

**默认值**：`0.0.0.0`

**选项**：

| 值 | 说明 | 适用场景 |
|----|------|---------|
| `0.0.0.0` | 监听所有网络接口 | 生产环境、允许外部访问 |
| `127.0.0.1` | 仅本机访问 | 开发环境、更安全 |

**示例**：
```env
# 生产环境
HOST=0.0.0.0

# 开发环境（更安全）
HOST=127.0.0.1
```

---

#### `PORT` (可选)

Web API 服务器端口。

**默认值**：`8000`

**常用端口**：`8000`, `8080`, `3000`, `5000`

**示例**：
```env
PORT=8080
```

---

#### `RELOAD` (可选)

是否启用代码自动重载。

**默认值**：`true`

**选项**：

| 值 | 说明 | 适用场景 |
|----|------|---------|
| `true` | 代码变更自动重启 | 开发环境 |
| `false` | 不自动重启 | 生产环境 |

**示例**：
```env
# 开发环境
RELOAD=true

# 生产环境
RELOAD=false
```

---

## 🤖 模型选择指南

### 推荐模型（2024年）

#### 🥇 最佳选择：GPT-4o

**适用**：所有场景

```env
SKILLNET_MODEL=gpt-4o
```

**优点**：
- ✅ 最新旗舰模型
- ✅ 性能强大
- ✅ 成本合理
- ✅ 128K 上下文

**定价**：
- 输入：$2.50 / 1M tokens
- 输出：$10.00 / 1M tokens

**预估成本**：创建一个技能 ≈ $0.05-0.20

---

#### 🥈 经济选择：GPT-4o Mini

**适用**：评估、分析等轻量任务

```env
SKILLNET_MODEL=gpt-4o-mini
```

**优点**：
- ✅ 速度快
- ✅ 成本低（约为 GPT-4o 的 1/15）
- ✅ 适合简单任务

**定价**：
- 输入：$0.15 / 1M tokens
- 输出：$0.60 / 1M tokens

**预估成本**：创建一个技能 ≈ $0.01-0.05

---

#### 🥉 高性能：GPT-4 Turbo

**适用**：复杂推理任务

```env
SKILLNET_MODEL=gpt-4-turbo
```

**优点**：
- ✅ 推理能力强
- ✅ 128K 上下文
- ✅ 稳定性好

**定价**：
- 输入：$10.00 / 1M tokens
- 输出：$30.00 / 1M tokens

**预估成本**：创建一个技能 ≈ $0.20-0.50

---

### 其他模型选项

#### OpenAI 系列

```env
# 经典 GPT-4
SKILLNET_MODEL=gpt-4

# 经济型
SKILLNET_MODEL=gpt-3.5-turbo
```

#### Claude 系列（需配置 BASE_URL）

```env
BASE_URL=https://api.anthropic.com/v1
SKILLNET_MODEL=claude-3-5-sonnet-20241022
```

可选型号：
- `claude-3-5-sonnet-20241022` - 最新版本
- `claude-3-opus-20240229` - 最强推理
- `claude-3-sonnet-20240229` - 平衡性能

#### 国产模型

**阿里通义千问**：
```env
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
SKILLNET_MODEL=qwen-max
```

**智谱清言**：
```env
BASE_URL=https://open.bigmodel.cn/api/paas/v4
SKILLNET_MODEL=glm-4
```

**百度文心一言**：
```env
BASE_URL=https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop
SKILLNET_MODEL=ERNIE-4.0-8K
```

**DeepSeek**：
```env
BASE_URL=https://api.deepseek.com/v1
SKILLNET_MODEL=deepseek-chat
```

---

### 场景推荐

| 功能 | 推荐模型 | 原因 |
|------|---------|------|
| **创建技能** | `gpt-4o`, `gpt-4-turbo` | 需要理解复杂上下文，生成高质量代码 |
| **评估技能** | `gpt-4o`, `gpt-4o-mini` | 需要多维度分析，但生成内容较少 |
| **分析关系** | `gpt-4o-mini`, `gpt-3.5-turbo` | 主要是分类匹配，轻量模型即可 |
| **批量操作** | `gpt-4o-mini` | 降低成本，速度快 |
| **高精度任务** | `gpt-4-turbo`, `claude-3-opus` | 需要最强推理能力 |

---

## 💡 配置示例

### 示例 1: 最小配置

**场景**：仅使用搜索和下载功能

```env
# 无需任何配置，直接使用！
```

**可用功能**：
- ✅ `skillnet search` - 搜索技能
- ✅ `skillnet download` - 下载技能
- ❌ `skillnet create` - 需要 API_KEY
- ❌ `skillnet evaluate` - 需要 API_KEY
- ❌ `skillnet analyze` - 需要 API_KEY

---

### 示例 2: 基础配置

**场景**：使用所有功能，标准网络环境

```env
# OpenAI API
API_KEY=sk-proj-abc123...
SKILLNET_MODEL=gpt-4o

# GitHub（可选但推荐）
GITHUB_TOKEN=ghp_abc123...
```

**可用功能**：
- ✅ 所有 CLI 功能
- ✅ 所有 Python SDK 功能
- ✅ Web API 服务

---

### 示例 3: 完整配置（国内环境）

**场景**：国内网络，使用所有功能

```env
# OpenAI API（使用代理）
API_KEY=sk-proj-abc123...
BASE_URL=https://api.openai-proxy.com/v1
SKILLNET_MODEL=gpt-4o

# GitHub 加速
GITHUB_TOKEN=ghp_abc123...
GITHUB_MIRROR=https://ghfast.top/

# Web API 服务器
HOST=0.0.0.0
PORT=8080
RELOAD=true
```

**特点**：
- ✅ 使用代理访问 OpenAI
- ✅ GitHub 镜像加速
- ✅ 完整功能支持

---

### 示例 4: 使用 Azure OpenAI

**场景**：企业环境，使用 Azure OpenAI

```env
# Azure OpenAI
API_KEY=your-azure-api-key
BASE_URL=https://your-resource.openai.azure.com/openai/deployments/gpt-4o
SKILLNET_MODEL=gpt-4o

# GitHub
GITHUB_TOKEN=ghp_abc123...

# Web API（仅内网访问）
HOST=127.0.0.1
PORT=8000
RELOAD=false
```

---

### 示例 5: 使用国产模型

**场景**：使用阿里通义千问

```env
# 阿里云百炼平台
API_KEY=sk-your-dashscope-api-key
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
SKILLNET_MODEL=qwen-max

# GitHub
GITHUB_TOKEN=ghp_abc123...
GITHUB_MIRROR=https://ghfast.top/
```

---

### 示例 6: 多环境配置

**开发环境** (`.env.development`):
```env
API_KEY=sk-test-key...
SKILLNET_MODEL=gpt-4o-mini
HOST=127.0.0.1
PORT=8000
RELOAD=true
```

**生产环境** (`.env.production`):
```env
API_KEY=sk-prod-key...
SKILLNET_MODEL=gpt-4o
HOST=0.0.0.0
PORT=8080
RELOAD=false
```

**使用方式**：
```bash
# 开发环境
cp .env.development .env

# 生产环境
cp .env.production .env
```

---

## ❓ 常见问题

### Q1: 我需要配置所有环境变量吗？

**A**: 不需要。根据您的使用场景选择：

- **仅搜索/下载**：无需配置
- **创建/评估/分析**：仅需 `API_KEY`
- **最佳体验**：`API_KEY` + `GITHUB_TOKEN` + `GITHUB_MIRROR`

---

### Q2: API_KEY 如何获取？

**A**: 
1. 访问 https://platform.openai.com/api-keys
2. 登录后点击 "Create new secret key"
3. 复制生成的 Key（以 `sk-` 开头）

**注意**：首次使用需要充值（最低 $5）

---

### Q3: GITHUB_TOKEN 必须配置吗？

**A**: 不是必需，但强烈推荐：

**不配置的影响**：
- API 速率限制：60次/小时（容易超限）
- 无法访问私有仓库
- 批量操作受限

**配置后的好处**：
- API 速率限制：5000次/小时
- 可访问私有仓库
- 批量操作流畅

---

### Q4: 国内网络无法访问 OpenAI 怎么办？

**A**: 有三种解决方案：

1. **使用代理服务**（推荐）
   ```env
   BASE_URL=https://api.openai-proxy.com/v1
   ```

2. **使用国产模型**
   ```env
   BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   SKILLNET_MODEL=qwen-max
   ```

3. **使用 Azure OpenAI**
   ```env
   BASE_URL=https://your-resource.openai.azure.com/...
   ```

---

### Q5: 如何选择合适的模型？

**A**: 根据场景选择：

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 日常使用 | `gpt-4o` | 最佳性价比 |
| 节省成本 | `gpt-4o-mini` | 便宜 15 倍 |
| 高精度任务 | `gpt-4-turbo` | 推理能力强 |
| 批量操作 | `gpt-4o-mini` | 快速且便宜 |

---

### Q6: .env 文件会被提交到 Git 吗？

**A**: 不会！`.env` 已在 `.gitignore` 中排除。

**安全提醒**：
- ✅ `.env.example` 可提交（不含密钥）
- ❌ `.env` 不可提交（含密钥）
- ✅ 定期轮换 API Key
- ❌ 不要在代码中硬编码密钥

---

### Q7: 如何验证配置是否正确？

**A**: 运行以下命令测试：

```bash
# 测试 API_KEY
skillnet create --prompt "创建一个测试工具" --output-dir ./test

# 测试 GITHUB_TOKEN
skillnet download <github-url>

# 测试 Web API
source .venv/bin/activate
python run_api.py
# 访问 http://localhost:8080/docs
```

---

### Q8: 如何估算使用成本？

**A**: 

**单次操作成本**（使用 gpt-4o）：
- 创建技能：$0.05 - $0.20
- 评估技能：$0.02 - $0.05
- 分析关系：$0.01 - $0.03

**月度预估**（中等使用）：
- 创建 50 个技能：$2.50 - $10.00
- 评估 100 个技能：$2.00 - $5.00
- 合计：约 $5 - $15/月

**节省成本建议**：
- 使用 `gpt-4o-mini` 替代 `gpt-4o`（节省 85%）
- 批量操作使用轻量模型
- 合理设置缓存

---

## 🔐 安全最佳实践

### 1. 保护您的密钥

```bash
# ✅ 好的做法
echo 'API_KEY=sk-...' > .env
chmod 600 .env  # 仅所有者可读写

# ❌ 不好的做法
export API_KEY=sk-...  # 容易泄露到 shell 历史
git add .env           # 千万不要提交到 Git
```

### 2. 定期轮换密钥

- OpenAI API Key：每 3-6 个月
- GitHub Token：每 6-12 个月
- 发现泄露：立即重新生成

### 3. 使用环境特定配置

```bash
# 开发环境
.env.development

# 生产环境
.env.production

# 测试环境
.env.test
```

### 4. 最小权限原则

**GitHub Token 权限**：
- ✅ 仅公开仓库：`public_repo`
- ✅ 私有仓库：`repo`
- ❌ 不需要：`admin`, `delete_repo`, `workflow`

---

## 📞 获取帮助

遇到问题？

1. 查看文档：`docs/`
2. 查看示例：`.env.example`
3. 运行测试：`python test_sdk.py`
4. 提交 Issue: https://github.com/zjunlp/SkillNet/issues

---

**最后更新**: 2026-04-04  
**版本**: SkillNet 0.0.17
