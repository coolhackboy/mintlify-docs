---
name: vidgo-api
description: Use when building integrations with the Vidgo API for image, video,
  audio, music, 3D, and LLM generation models. Reach for this skill when
  submitting generation tasks, polling task status, handling webhooks, uploading
  files, checking credits, or handling errors in asynchronous API workflows.
metadata:
  author: vidgo
  version: "1.0"
---

# Vidgo API Skill

## Product Summary

Vidgo API gives one API key access to image, video, audio, music, 3D, and LLM models. Generation models (image, video, audio, music, 3D) use an asynchronous submit-and-query workflow: POST to `/api/generate/submit` with a `model` ID and an `input` object, receive a `task_id`, then poll `GET /api/generate/status/{task_id}` or pass a `callback_url` to receive a webhook. LLM models use OpenAI-, Claude-, and Gemini-compatible endpoints.

- Base URL: `https://api.vidgo.ai`
- Authentication: `Authorization: Bearer VIDGO_API_KEY`
- API keys: https://vidgo.ai/apis/dashboard/api-key
- Generated files are valid for 24 hours; download and store results promptly.

## When to Use

- **Submitting generation tasks**: image, video, audio, music, or 3D generation
- **Polling task status**: checking whether a task has finished
- **Implementing webhooks**: receiving task completion callbacks
- **Handling errors**: retrying rate limits and transient failures, handling insufficient credits
- **Checking account balance**: verifying credits before expensive tasks
- **Uploading files**: preparing images or audio for editing or reference workflows
- **LLM requests**: calling chat models through compatible endpoints

## Quick Reference

### Core Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/generate/submit` | POST | Submit an image, video, audio, music, or 3D task |
| `/api/generate/status/{task_id}` | GET | Query task status and result files |
| `/api/user/balance` | GET | Query remaining credits |
| `/api/common/upload/url` | POST | Upload a file from a remote URL |
| `/api/common/upload/base64` | POST | Upload a base64 data URL |
| `/api/common/upload/stream` | POST | Upload a file as a stream |
| `/v1/chat/completions` | POST | OpenAI Chat Completions compatible |
| `/v1/responses` | POST | OpenAI Responses compatible |
| `/v1/messages` | POST | Claude Messages compatible |
| `/v1beta/models/{model}:generateContent` | POST | Gemini native format |

### Submit a Task

```bash
curl -X POST https://api.vidgo.ai/api/generate/submit \
  -H "Authorization: Bearer $VIDGO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/veo3.1-lite/text-to-video",
    "input": {
      "prompt": "A quiet forest under soft morning light",
      "duration": 6,
      "aspect_ratio": "16:9"
    },
    "callback_url": "https://your-domain.com/callback"
  }'
```

Keep `model` and `callback_url` at the request root and put model parameters inside `input`. Each model accepts different `input` fields; unsupported fields are rejected, so check the model's page in the docs before sending.

### Query Status

```bash
curl https://api.vidgo.ai/api/generate/status/TASK_ID \
  -H "Authorization: Bearer $VIDGO_API_KEY"
```

| Status | Meaning | Action |
|--------|---------|--------|
| `not_started` | Queued | Keep polling |
| `running` | Generating | Keep polling |
| `finished` | Complete, results in `files` | Download every file |
| `failed` | Failed, reason in `error_message` | Inspect the error before retrying |

```json
{
  "code": 200,
  "data": {
    "task_id": "task-unified-1757165031-uyujaw3d",
    "status": "finished",
    "progress": 100,
    "files": [
      { "file_url": "https://...", "file_type": "image" }
    ],
    "created_time": "2025-11-12T10:30:00",
    "error_message": null
  }
}
```

### Example Model IDs

| Category | Model ID |
|----------|----------|
| Image | `alibaba/z-image/turbo`, `gpt-4o-image` |
| Video | `google/veo3.1-lite/text-to-video`, `kwaivgi/kling-v3.0-std/text-to-video` |
| Music | `generate-music` |
| LLM | `openai/gpt-6-astra` (via `/v1/chat/completions`) |

The full, current model list and each model's parameters are in the docs navigation (https://docs.vidgo.ai/llms.txt).

## Workflow

1. **Prepare**: pick a model ID, read its docs page, and build `input` with only the supported fields.
2. **Submit**: POST to `/api/generate/submit`; save the returned `data.task_id` immediately.
3. **Wait**: poll `/api/generate/status/{task_id}` every few seconds, or wait for the POST to your `callback_url`. Set an overall timeout so polling cannot loop forever.
4. **Handle the result**: on `finished`, download every entry in `files` (there can be more than one); on `failed`, log `error_message`.
5. **Store**: keep the files on your own storage; Vidgo file URLs expire after 24 hours.

## Common Gotchas

- **API key exposure**: never commit keys; read them from an environment variable such as `VIDGO_API_KEY`.
- **Retrying creates a new paid task**: check the status of the original `task_id` before resubmitting.
- **Credits**: credits are deducted at submission and refunded automatically if the task fails.
- **Webhooks**: respond with HTTP 2xx within 30 seconds and process asynchronously. Failed deliveries are retried up to 5 times (60, 120, 240, 480, 600 seconds); `4xx` responses are not retried. Make the handler idempotent. Polling still works if every callback fails.
- **Public URLs only**: image, audio, and video inputs must be publicly reachable HTTP(S) URLs; upload local files first.
- **Rate limits**: back off exponentially on `429`.

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Invalid parameters, or insufficient credits on task submission | Fix the request against the model docs; check the balance |
| 401 | Missing or invalid API key | Check the `Authorization` header |
| 402 | Insufficient credits on LLM endpoints | Top up the balance |
| 429 | Rate limited | Retry with exponential backoff |
| 500, 502, 503 | Server or upstream error | Retry with backoff; contact support if it persists |

## Resources

- Docs index: https://docs.vidgo.ai/llms.txt
- Quick start: https://docs.vidgo.ai/api-manual/quickstart
- Task status: https://docs.vidgo.ai/api-manual/task-management/status
- Webhooks: https://docs.vidgo.ai/api-manual/task-management/webhooks
- Error codes: https://docs.vidgo.ai/api-manual/error-codes
- Agent setup: https://vidgo.ai/apis/agent-setup
