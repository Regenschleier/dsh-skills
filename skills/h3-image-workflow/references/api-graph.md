# API 图骨架（可直接提交）

把下面 JSON 里的 `PROMPT`、`seed`、`ref.png` 换掉即可 `POST http://127.0.0.1:8188/prompt`，
请求体是 `{"prompt": { ...下面的节点... }}`。

## 带参考图（锁身份，vae 接着）

```json
{
  "1":  { "class_type": "UNETLoader",
          "inputs": { "unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors", "weight_dtype": "default" } },
  "2":  { "class_type": "ModelAttentionBackend",
          "inputs": { "model": ["1", 0], "attention": "comfy kitchen attention" } },
  "3":  { "class_type": "CLIPLoader",
          "inputs": { "clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors", "type": "minimax" } },
  "5":  { "class_type": "VAELoader",
          "inputs": { "vae_name": "minimax_h3_video_vae_fp16.safetensors" } },
  "7":  { "class_type": "LoadImage", "inputs": { "image": "ref.png" } },
  "6":  { "class_type": "MiniMaxH3ImageConditioning",
          "inputs": {
            "clip": ["3", 0],
            "vae": ["5", 0],
            "prompt": "PROMPT",
            "width": 768,
            "height": 1344,
            "images.image_0": ["7", 0]
          } },
  "8":  { "class_type": "RandomNoise", "inputs": { "noise_seed": 1 } },
  "9":  { "class_type": "KSamplerSelect", "inputs": { "sampler_name": "res_multistep" } },
  "10": { "class_type": "BasicScheduler",
          "inputs": { "model": ["2", 0], "scheduler": "simple", "steps": 30, "denoise": 1 } },
  "11": { "class_type": "BasicGuider",
          "inputs": { "model": ["2", 0], "conditioning": ["6", 0] } },
  "12": { "class_type": "SamplerCustomAdvanced",
          "inputs": { "noise": ["8", 0], "guider": ["11", 0], "sampler": ["9", 0],
                      "sigmas": ["10", 0], "latent_image": ["6", 1] } },
  "13": { "class_type": "LTXVSeparateAVLatent", "inputs": { "av_latent": ["12", 0] } },
  "14": { "class_type": "VAEDecode", "inputs": { "samples": ["13", 0], "vae": ["5", 0] } },
  "15": { "class_type": "SaveImage", "inputs": { "images": ["14", 0], "filename_prefix": "h3ref/out" } }
}
```

## 出 CG：只删一行

把节点 `"6"` 里的 `"vae": ["5", 0]` 整条删掉。`VAEDecode` 的 `vae` **保留**。
区别：接 vae 时参考图被编码成 `minimax_refs` latent（权重压过文字，脸是真人五官）；
不接时参考图只进文本编码器（画面跟提示词走，变瓷面 CG）。

## 换机位：再删一个键

把节点 `"6"` 里的 `"images.image_0": ["7", 0]` 删掉（`"7"` 这个 LoadImage 节点可以留着不连）。
此时人物必须完全用文字重写，提示词里不要再出现 `<Picture 1>`。

## 常见改法

- **换种子**：改 `"8".inputs.noise_seed`。
- **换输出目录**：改 `"15".inputs.filename_prefix`，例如 `h3ref/mor3_A2`。
- **改尺寸**：`width/height` 必须是 32 的倍数，且 `width*height ≤ 1032192`（=768×1344）。
- **不要 AV 分支**：`LTXVSeparateAVLatent` 的第 1 输出（audio_latent）在静帧流程里不用，别接 `VAEDecodeAudio`。

## 为什么必须过 `LTXVSeparateAVLatent`

`MiniMaxH3ImageConditioning` 输出的 latent 是 `[1, 24, 1, h/16, w/16]` 的普通 samples，
采样器 `SamplerCustomAdvanced` 吐出来的却是 AV 嵌套结构，所以要先拆一次、只取第 0 输出 `video_latent` 再解码。

## 提交方式（这一步写错会直接被拒）

`POST /prompt` 的请求体必须是**包了一层 `prompt`** 的对象：

```powershell
# 把 nodes.json 换成你的节点表（就是下面这段 JSON 本身，或界面里「Save (API Format)」导出的文件）
$nodes = Get-Content "nodes.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$body  = @{ prompt = $nodes } | ConvertTo-Json -Depth 20 -Compress
[System.IO.File]::WriteAllText("$PWD\body.json", $body, (New-Object System.Text.UTF8Encoding($false)))
$cli = New-Object System.Net.WebClient
$cli.Encoding = [System.Text.Encoding]::UTF8
$cli.Headers.Add("Content-Type", "application/json")
$cli.UploadString("http://127.0.0.1:8188/prompt", "POST", (Get-Content "body.json" -Raw -Encoding UTF8))
```

界面导出的 API 文件是**裸节点表**，直接 POST 会报缺少 `prompt` 字段，所以要自己包一层。

## 报错对照（只列实测过的）

| 报错 / 现象 | 原因 | 改法 | 验证 |
|---|---|---|---|
| `execute() got an unexpected keyword argument 'image_0'. Did you mean 'images'?` | autogrow 槽位键少了 `images.` 前缀 | 写成 `"images.image_0"` | 实测 |
| 请求被拒 / 提示缺少 `prompt` | 把裸节点表直接 POST 了 | 外面包一层 `{"prompt": {...}}` | 实测（本 skill 手册第一版就写错在这里） |
| 出图约 1.8 MP，8 GB 卡爆显存 | `width/height` 留 0，按参考图短边 1024 自动出画布 | 显式写 768×1344 | 源码常量 `IMAGE_REF_SHORT_EDGE=1024` 推得，**未实测** |

