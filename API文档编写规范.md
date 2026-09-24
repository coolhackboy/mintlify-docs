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

只保留字符串类型和示例模型值。必填要求由请求体的 `required` 声明；不添加重复的标识说明或 `enum` 可选值列表。多模型接口的其他可用模型放在模型列表或请求示例中。

```json
"model": {
  "type": "string",
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

### 4. 计费说明

- 只说明影响计费的模型档位和参数，例如分辨率、质量、时长、输出数量、音频开关、参考图片数量或参考视频时长；按各模型实际规则填写。
- 不在 MDX 正文、OpenAPI 描述或示例标题中写具体金额、积分单价、计费倍率、积分兑换比例、价格对比、折扣百分比或带具体价格的计算示例。
- 保留按次、按张、按时长等计费方式，以及时长取整、参考素材附加费用、扣费和退款规则。需要查询实时价格时可链接价格页。

### 5. 参数说明范围

- MDX 正文和 OpenAPI 描述只说明当前接口 schema 中存在的字段，不逐项列出其他接口才有的“不支持字段”。
- 按当前工作流核对通用文案，避免将图片上传、视频分镜或 `prompt` / `text` 等说明复制到没有对应入参的接口。
- 保留实际支持字段之间的依赖、互斥和取值限制；区分请求参数、响应字段与其他接口的使用指引。

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
- [ ] 计费说明仅列影响因素和规则，正文、OpenAPI 与示例中没有具体价格
- [ ] 正文和 OpenAPI 描述中的入参均属于当前接口，实际参数约束完整
- [ ] docs.json 已更新 openapi 和 navigation
