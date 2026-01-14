# Vidgo API 文档编写规范

以 `/api-manual/music-series/generate-music` 为模板，后续新建 API 文档时请遵循以下规则。

---

## 一、文件结构

每个 API 需要创建两个文件：

```
api-manual/{series-name}/
├── {api-name}.json    # OpenAPI 3.0.0 规范文件
└── {api-name}.mdx     # MDX 文档文件
```

同时需要更新 `docs.json` 配置文件。

---

## 二、命名规范

### 1. 文件/文件夹命名
- 使用 **kebab-case**（小写 + 连字符）
- 示例：`generate-music.json`, `music-series/`

### 2. 参数命名
- 使用 **snake_case**（蛇形命名）
- 示例：`callback_url`, `custom_mode`, `style_weight`

### 3. API Key 占位符
- 使用 `VIDGO_API_KEY`（不是 `YOUR_API_KEY` 或 `<token>`）

---

## 三、请求体结构（统一格式）

```json
{
  "model": "{api-model-name}",           // 必填，API 模型标识符
  "callback_url": "https://...",         // 可选，Webhook 回调 URL
  "input": {
    // 具体参数放在 input 内
  }
}
```

### 关键点：
- `model` 和 `callback_url` 放在请求体一级
- 其他业务参数放在 `input` 对象内

---

## 四、响应体结构（统一格式）

### 成功响应 (200)
```json
{
  "code": 200,
  "data": {
    "task_id": "task-unified-xxx",
    "status": "not_started",
    "created_time": "2025-11-12T10:30:00"
  }
}
```

### 错误响应 (400/401)
```json
{
  "code": 400,
  "error": {
    "message": "Invalid request parameters",
    "type": "invalid_request_error"
  }
}
```

---

## 五、OpenAPI JSON 文件规范

### 1. 基本结构
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Vidgo API - {API Name}",
    "description": "{简短描述}",
    "version": "1.0.0"
  },
  "servers": [{ "url": "https://api.Vidgo API.ai" }],
  "security": [{ "BearerAuth": [] }],
  "paths": { ... },
  "components": { ... }
}
```

### 2. 参数描述格式
参数描述需要**换行分段**，便于阅读：

```json
"description": "主描述。\n\n- 条件1：说明...\n\n- 条件2：说明...\n\n**Note**: 注意事项"
```

#### 示例：
```json
"custom_mode": {
  "type": "boolean",
  "description": "Enable advanced parameter customization mode.\n\n- When `true`: Enables full control over style, title, and other parameters. `style` and `title` become required fields.\n\n- When `false`: Simplified mode where only `prompt` is needed. Lyrics will be automatically generated based on your prompt.",
  "example": true
}
```

### 3. 避免重复 Example
如果已有 `"example": "xxx"` 字段，description 中不要再写 `Example: "xxx"`

### 4. 外层 model 参数
```json
"model": {
  "type": "string",
  "description": "API model identifier.\n\nMust be `{api-model-name}` for this endpoint.",
  "enum": ["{api-model-name}"],
  "example": "{api-model-name}"
}
```

### 5. 提供多个 examples
在 `requestBody.content.application/json.examples` 中提供多个使用场景：
```json
"examples": {
  "example-1": {
    "summary": "场景1描述",
    "value": { ... }
  },
  "example-2": {
    "summary": "场景2描述",
    "value": { ... }
  }
}
```

---

## 六、MDX 文档文件规范

### 1. 文件头 (frontmatter)
```yaml
---
title: "{API 名称}"
description: "{简短描述}"
openapi: "/api-manual/{series}/{api-name}.json POST /api/generate/submit"
---
```

### 2. 文档结构（按顺序）

#### Usage Guide
```markdown
## Usage Guide

- 功能说明1
- 功能说明2
- 功能说明3
```

#### Parameter Details
```markdown
## Parameter Details

- In Custom Mode ( `custom_mode: true` ):
  - 条件说明...
  - 字符限制...

- In Non-custom Mode ( `custom_mode: false` ):
  - 条件说明...
```

#### Developer Notes
```markdown
## Developer Notes

- 使用建议或注意事项
```

#### Optional parameters
```markdown
## Optional parameters

- `param_name` (type): 参数说明...
- `param_name` (type): 参数说明...
```

### 3. 不需要的章节
以下内容由 OpenAPI 自动生成，MDX 中**不需要**写：
- Request Example
- Response Example
- Code Examples (cURL/Python/JavaScript 等)
- Available Models 表格（除非有特殊说明需求）
- Next Steps

---

## 七、更新 docs.json

### 1. 添加 OpenAPI 文件引用
```json
"openapi": [
  ...existing files...,
  "/api-manual/{series}/{api-name}.json"
]
```

### 2. 添加导航
```json
{
  "group": "{Series Name}",
  "pages": [
    "api-manual/{series}/{api-name}"
  ]
}
```

---

## 八、检查清单

创建新 API 文档时，请确认：

- [ ] 文件命名使用 kebab-case
- [ ] 参数命名使用 snake_case
- [ ] 请求体结构：model + callback_url 在一级，其他参数在 input 内
- [ ] 响应体结构与图片/视频系列一致
- [ ] JSON 参数描述有换行分段
- [ ] 没有重复的 Example
- [ ] API Key 使用 `VIDGO_API_KEY`
- [ ] MDX 包含 Usage Guide、Parameter Details、Developer Notes、Optional parameters
- [ ] docs.json 已更新 openapi 和 navigation
