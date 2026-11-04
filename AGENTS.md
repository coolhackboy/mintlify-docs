# Vidgo API 文档

写新的 API 文档、修改页面或翻译前先读本文件。本仓库的版式与 PoYo 文档（`c:\code\docs`）对齐，但品牌、域名、API Key 占位符和模型 ID 都是 Vidgo 自己的。本文件取代旧的 `API文档编写规范.md`（保留作历史参考，两者冲突时以本文件为准）。

## 站点结构

- Mintlify `theme: mint`，字体 Geist，代码块深色，主色 `#3B82F6` 系（`colors` 不改）。站点名 `Vidgo API`。不要引入 PoYo 的名称、Logo、链接或 Discord。
- 顶部 Tab（`docs.json` → `navigation.languages[].tabs`）：

| Tab | 内容 | 目录 |
| --- | --- | --- |
| Platform | 入门、错误码、任务管理、文件管理、账户、FAQs | 根目录 `index.mdx`、`faqs.mdx`，`api-manual/*.mdx`、`task-management/`、`file-series/`、`account-management/`，Suno 的 `query-music-detail` / `music-webhook` |
| Image Models | 图像生成/编辑 | `api-manual/image-series/` |
| Video Models | 视频生成 | `api-manual/video-series/` |
| Audio Models | TTS / 语音 | `api-manual/music-series/`（与 PoYo 一样 TTS 文件放在 music-series，不新建 audio 目录） |
| LLM Models | Chat 协议页 | `api-manual/chat-series/` |
| 3D Models | 3D 生成 | `api-manual/3d-series/` |
| Music Models | Suno 动作页、MiniMax Music、ElevenLabs Music | `api-manual/music-series/` |

- 每个模型 Tab 的第一个分组与 Tab 同名，第一页是该类的 `overview`（Audio 是 `music-series/audio-overview`），后面按厂商分子组（OpenAI、Google、Flux、Kling、Alibaba、MiniMax / Hailuo、Seedance……）。新页面放进对应厂商子组；没有就新建子组。
- 概览页（`*/overview.mdx`、`audio-overview.mdx`）的 `## Models` 表要随页面增减同步：一行一个页面，列 `Model`（页面标题加链接）、`Provider`（侧栏子组名）、`Model IDs`（OpenAPI 里的 `model`，多个用 `<br />` 分隔）。
- 页面移动或改名时，在 `docs.json` 的 `redirects` 里加旧 URL → 新 URL（`permanent: true`），不要让旧链接 404。

## 生成类模型页

### 适用范围

用于 image / video / 3D / TTS / 非 Suno 音乐的生成模型页。以下页面保持各自模板，不套用本节的 `##` 顺序：`chat-series/`、Suno 动作页（`generate-music`、`extend-music`、`add-vocals`、`vocal-remover/*` 等）、任务管理、文件、账户页。

### 文件与命名

每个页面一对同名文件，kebab-case：

```
api-manual/{series}/{name}.mdx
api-manual/{series}/{name}.json
```

Vidgo 的公开 model ID 多为 `provider/model/mode`，通常**一个 mode 一页**。`name` 由公开 ID 把 `/` 和 `.` 换成 `-` 得到，例如 `kwaivgi/kling-v3.0-std/text-to-video` → `kwaivgi-kling-v3-0-std-text-to-video`，`google/veo3.1/text-to-video` → `google-veo3-1-text-to-video`。同一模型的几个 mode 几乎完全相同时，可以合成一页、在 JSON 的 `model` 里列出全部 ID（参考 `nano-banana-2`、`kling-3-0` 这类家族页）。

在 `docs.json` 登记三处：

1. `api.openapi` 追加 `"/api-manual/{series}/{name}.json"`（英文）和 `"/zh/api-manual/{series}/{name}.json"`（中文 JSON 存在后）。
2. `en` 导航对应 Tab → 厂商子组的 `pages` 追加 `"api-manual/{series}/{name}"`（不带扩展名）。
3. `zh` 导航见下文「中文文档」。

### 请求体与 OpenAPI

- OpenAPI `3.0.0`；`info.title` 写 `Vidgo API - {页面标题}`；`servers` 为 `[{"url": "https://api.vidgo.ai", "description": "Production server"}]`；`security` 为 `BearerAuth`。
- `securitySchemes.BearerAuth.description` 写 ``Use `Authorization: Bearer VIDGO_API_KEY`.``，可补充 Key 的创建入口 **Dashboard → API Key**（`https://vidgo.ai/apis/dashboard/api-key`）。
- API Key 占位符一律 `VIDGO_API_KEY`（cURL 里用 `$VIDGO_API_KEY`），不要写 `YOUR_API_KEY`、`<token>` 或 `PoYo_API_KEY`。
- 请求体只有三个顶层字段：必填 `model`、可选 `callback_url`、`input`。业务参数全部放进 `input`，参数名 snake_case。
- `model` 字段：`type: string` + 该页的 `example`（家族页可用 `enum` 列出全部 ID）。
- 提交成功响应 `code: 200`，`data` 含 `task_id`、`status: not_started`、`created_time`。400 / 401 的错误体以 [Error Codes](/api-manual/error-codes) 为准（生成接口返回 `{"detail": "..."}`），不要照抄 PoYo 的 `error.message` 结构。
- 参数说明写在 `description`，可用 `\n\n` 分段；已有 `example` 时 description 里不再写 Example。
- URL 参数（含数组 `items`）用 `type: string` + `format: uri`，「公开可访问的 HTTP/HTTPS」写在 description。
- 不使用 `pattern`（Mintlify 会额外显示 Pattern）；保留 `minLength`、`maxLength`、`minimum`、`maximum`、`enum`、`default`、`format`。
- `requestBody.content.application/json.examples` 至少给出每种输入模式一个示例。
- 只描述当前接口 schema 里存在的字段，不列「其他接口才有、本接口不支持」的字段。

### Frontmatter

```yaml
---
title: "Kling 3.0 Std Text to Video"
description: "The Kling 3.0 Std Text to Video API turns a prompt into a 3–15 second 720p video with optional native audio and multi-shot prompts."
icon: "video"
openapi: "/api-manual/video-series/kwaivgi-kling-v3-0-std-text-to-video.json POST /api/generate/submit"
---
```

- `title` 只写模型名（一页一个 mode 时加上 mode，如 `Text to Video`、`Image Edit`）。不要追加 Generation、Video Generation、Image Generation、API。
- `icon`：图像 `image`，视频 `video`，3D `cube`，TTS / 音乐 `music` 或 `volume-high`。
- `openapi` 的文件、方法、path 与 JSON 一致，并且总是带文件路径（多个 spec 定义了同一 path，省略文件会解析到错误的 spec）。

### 正文

不写与 `title` 重复的 `# 一级标题`。正文第一块是固定任务提示，原文不改：

```mdx
<Tip>
1. After submission, a `task_id` will be returned. If you provided a `callback_url`, when the task status becomes `finished` or `failed`, a POST request will be sent to the `callback_url`.
2. Regardless of whether `callback_url` is provided, you can retrieve the result through the unified [Query Task Status](/api-manual/task-management/status) endpoint.
</Tip>
```

（Suno 动作页把第 2 条的链接换成 [Query Music Detail](/api-manual/music-series/query-music-detail)。）

紧接一段简短介绍：模型能生成什么、适合什么场景。

### 二级标题顺序

按顺序写，没有内容的节整节省略：

1. `## Models` — 每个公开 model ID 一条：`- **provider/model/mode** — 一句说明`。只有一个也用这个标题。不要用 Available Models / Available Model / Model。
2. `## Features` — 能力。替代 Key Features、Capabilities。
3. `## Input modes` — 仅当有互斥工作流（文生 vs 图生、首帧 vs 参考图等）时写。
4. `## Required parameters` — `input` 必填字段，每条 `` `param_name` (type): 说明 ``。
5. `## Optional parameters` — `input` 可选字段。
6. 领域小节（仅需要时，放在可选参数之后）：`## Size`、`## Resolution`、`## Duration`、`## Output`、`## Output Formats`、`## Voice Presets`。
7. `## Examples` — 场景要点，对应 OpenAPI examples。
8. `## Notes` — 限制、互斥、失败条件、计费规则说明。

历史页面里的 `Advanced Parameters`、`Duration Options`、`Output Options`、`Workflow IDs`、`Parameter Details`、`Usage Guide` 等节已被批量挪到第 5 与第 7 之间，内容未删。改到这些页面时顺手合并进上面的标准小节。

### 计费

- 不写具体金额、积分单价、倍率、折扣或带价格的计算示例；价格只在 [定价页](https://vidgo.ai/apis/api-pricing)。
- 影响计费的因素（分辨率、时长、张数、音频开关、参考素材时长、失败退款）可以写，统一放在 `## Notes` 的一条 bullet 里。历史页面里单独的 `## Pricing` / `## Billing` / `## Billing Factors` 节是旧写法，改页时并入 `## Notes`。
- 任务状态响应里的 `credits_amount` 等是 API 字段，可以保留。

## LLM 页面

`chat-series/` 下：`overview.mdx`（全量模型表：model ID × 支持的协议），以及按协议的格式页 `chat-completions`、`responses`、`claude-messages`、`gemini-native-format`（各配一个 JSON）。新增 LLM 模型时：在 `overview.mdx` 表里加一行，并把 ID 加到它支持的每个格式 JSON 的 `model` `enum`/示例里。不写价格。若以后按厂商拆页，沿用 PoYo 的 `{provider}.mdx/.json` 写法并放到 LLM Models → `Models` 子组。

## SEO

- `title`：模型名（+ mode），不超过约 60 个字符；Mintlify 会自动追加站点名，不要手写「| Vidgo API」。同一模型的多个 mode 页标题必须能区分。
- `description`：一句话，约 120–160 个字符，以 `The {Model} API …` 开头，写清输入、输出和关键规格（时长范围、分辨率、是否带音频、参考图数量等）。每页唯一，不要多页复用同一句；不写价格、不堆关键词、不写「best / cheapest」。
- 中文 `description` 对应翻译，以「{Model} API …」开头，同样写规格。
- 正文第一段自然地出现模型名和主要任务（如「文生视频」）。图片要有 alt 文本。
- 内链用站内绝对路径（`/api-manual/...`），不要用完整域名。

## 中文文档（zh）

英文是源语言，文件在仓库根目录，URL 不带前缀。中文文件放在 `zh/` 下，路径与英文一一对应：`api-manual/video-series/kling-3-0.mdx` ↔ `zh/api-manual/video-series/kling-3-0.mdx`。翻译人工完成，不写调用 LLM 的脚本批量翻译。

### 现状与导航策略

- 已翻译：Platform Tab 全部页面（`zh/index`、quickstart、workflow-guide、error-codes、任务管理、Suno 音乐任务查询 / Webhook、文件管理、账户、FAQs）、`zh/openapi.json`，以及每个模型 Tab 的概览页（含 `zh/api-manual/chat-series/overview`）。
- 模型页尚未翻译。`docs.json` 的 `zh` 导航**只登记已存在的 zh 页面**：每个模型 Tab 目前只有概览页一个分组，避免 Mintlify 构建时出现缺失页面或空分组。（PoYo 的 zh 树是英文导航的完整镜像；Vidgo 在翻译完成前按「只列已翻译页」逐步逼近同样的镜像。）
- 未翻译页面在 zh 页面里的链接暂时指向英文路径（不带 `/zh`），翻译后再改成 `/zh/...`。

### 翻译一个模型页的步骤

1. 新建 `zh/{英文路径}.mdx` 与 `zh/{英文路径}.json`。
2. 中文 frontmatter 的 `openapi` 指向中文 JSON：`"/zh/api-manual/{series}/{name}.json POST /api/generate/submit"`。
3. `docs.json`：`api.openapi` 追加 `"/zh/api-manual/{series}/{name}.json"`；在 `zh` 导航的同一 Tab 下，按英文的分组结构插入 `"zh/api-manual/{series}/{name}"`。分组不存在就按英文顺序新建（厂商名不译，Tab/分组名见下表），页面顺序与英文一致。
4. 更新该 Tab 的 zh 概览页表格链接：`/api-manual/...` → `/zh/api-manual/...`。
5. `grep -rn "(/api-manual/{series}/{name})\|\"/api-manual/{series}/{name}\"" zh/`，把其他 zh 页面里指向该页英文版的链接改成 `/zh/...`。
6. 运行 `python scripts/validate_docs.py` 和 `mint validate`，都通过再提交。

导航名称译法：Platform → 平台；Overview → 概览；Task Management → 任务管理；All Tasks → 全部任务；Music → 音乐；File Management → 文件管理；Account Management → 账户管理；FAQs → 常见问题；Image Models → 图像模型；Video Models → 视频模型；Audio Models → 音频模型；LLM Models → LLM 模型；3D Models → 3D 模型；Music Models → 音乐模型；API Formats → API 格式；Vocal Remover → 人声分离。厂商子组（OpenAI、Google、Flux、Seedream、Kling、Alibaba、Grok (xAI)、MiniMax / Hailuo、Runway、Seedance、Suno AI、ElevenLabs、Meshy、Hunyuan3D、Tripo3D、xAI、MiniMax）保持英文。

新增或修改英文页时，若中文页已存在，同步修改中文 MDX 和 JSON。

### 翻译规则

- Frontmatter：只翻译 `title`、`description`、`sidebarTitle`；`openapi`、`icon` 等原样保留（`openapi` 只把文件路径换成 `/zh/...`）。标题是模型名、厂商名或产品名时不翻译；mode 部分翻译，例如 `Kling 3.0 Std Text to Video` → `Kling 3.0 Std 文生视频`。
- 代码块（含行内代码、代码注释、JSON 示例中的 prompt）整块原样保留。
- 不翻译：model ID、参数名、字段名、枚举值、HTTP 方法与状态码、URL、产品与厂商名、`task_id` / `callback_url` 等 API 术语、`VIDGO_API_KEY`。
- 站内链接加 `/zh` 前缀（目标 zh 页存在时）；外部链接（`https://vidgo.ai/...`、`https://api.vidgo.ai`）不改。
- 锚点：标题翻译后，把 `#anchor` 改成中文标题生成的 slug（小写、去标点、空格变 `-`、保留中文）。
- MDX 组件标签和属性名不变，只翻译给人看的属性文字（`<Card title="...">`、`<Accordion title="...">`）。`href`、`icon` 不变。
- 表格、列表、标题层级、段落顺序与英文一致，不增删内容。HTTP 状态码小标题（`### 400 - Bad Request`）保持英文。
- 简体中文，中英文之间不强制加空格，中文句子用全角标点。
- OpenAPI 中文 JSON：结构与英文完全一致，只翻译 `description`、`summary`、`title` 的字符串；`enum`、`example`、`examples[].value`、`default`、`operationId`、`tags`、属性名都不改。字符串里的 Markdown 结构保留，站内链接同样加 `/zh`。securitySchemes 写 **仪表盘 → API 密钥**，链接与英文相同（Vidgo 暂无独立的中文仪表盘地址）。

### 固定译法

开头任务提示统一译为：

```mdx
<Tip>
1. 提交后会返回 `task_id`。如果提供了 `callback_url`，当任务状态变为 `finished` 或 `failed` 时，系统会向 `callback_url` 发送 POST 请求。
2. 无论是否提供 `callback_url`，都可以通过统一的[查询任务状态](/zh/api-manual/task-management/status)接口获取结果。
</Tip>
```

二级标题：Models → 模型；Features → 功能；Input modes → 输入模式；Required parameters → 必填参数；Optional parameters → 可选参数；Size → 尺寸；Resolution → 分辨率；Duration → 时长；Output → 输出；Output Formats → 输出格式；Voice Presets → 预设音色；Examples → 示例；Notes → 注意事项；Workflow → 工作流程。

术语：task → 任务；callback / webhook → 回调 / Webhook；text-to-image → 文生图；image-to-image → 图生图；image edit → 图像编辑；text-to-video → 文生视频；image-to-video → 图生视频；reference-to-video → 参考生视频；video edit → 视频编辑；first-last frame → 首尾帧；keyframes → 关键帧；motion control → 动作控制；extend → 扩展；text-to-speech / TTS → 文本转语音（TTS）；voice → 音色；lyrics → 歌词；vocals → 人声；instrumental → 伴奏；cover → 翻唱；text-to-3D → 文生 3D；image-to-3D → 图生 3D；multiview → 多视图；texture → 纹理；rigging → 骨骼绑定；prompt → 提示词；negative prompt → 负面提示词；aspect ratio → 宽高比；duration → 时长；resolution → 分辨率；seed → 种子；safety checker → 安全检查；API Key 保持 `API Key`；endpoint → 接口；playground 保持 Playground；credits → 积分；agent 保持 `Agent`。

## 校验

- `python scripts/validate_docs.py`：docs.json 合法、导航页面存在且不重复、zh 导航只含 zh 页、`api.openapi` 文件存在且是合法 JSON、frontmatter `openapi` 能解析到 spec/方法/path、站内链接都指向存在的页面。
- `mint validate`：Mintlify 构建校验。
- `mint broken-links` 在 Windows 上会把几乎所有站内链接误报为 broken（PoYo 仓库同样如此），在 Windows 上以 `validate_docs.py` 为准。
- 提交前确认 OpenAPI 中没有 `pattern`：`grep -rl '"pattern"' api-manual zh`。
