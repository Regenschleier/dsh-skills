# Krea2 模型与 LoRA 的下载来源（本机可达性实测）

验证日期 2026-11-22 / 23。所有「可达」都是当场 `Invoke-WebRequest` / `curl` 实测 200 且能下载完，不是听说。

## 一、可达性一览

| 站点 | 状态 | 备注 |
|---|---|---|
| `modelscope.cn` | ✅ 最快 | 实测 18.6 MB/s（Krea2 int8 三件套即从此下载） |
| `hf-mirror.com` | ✅ 可用 | 2.5–3 MB/s 起，能下 safetensors |
| `huggingface.co` | ❌ | 直连超时；302 规则里虽有 `huggingface` 段，但 302 当前未生效 |
| `civitai.com` | ❌ | 全线超时/连接重置 |
| `seaart.ai` / `seaart.me` / `seaart.cn` | ❌ | 10054 连接重置；浏览器打开直接 `chrome-error://chromewebdata/` |
| `tensor.art` / `tensorhub` | ❌ | 超时 |
| `civarchive.com` | ✅ 可读 | Civitai 删除模型的档案页（含 sha256、原文件名、是否 deleted） |
| `civitaiarchive.com` | ⚠️ 半可用 | 只是镜像站，接口 404 |
| `liblib.art` | ⚠️ 首页可达 | 搜索 API 需签名，未签名一律 `{"code":500,"msg":"模型查询失败"}` |
| `www.haiyi.art`（海艺） | ✅ 可达 | `POST /api/v1/model/list` + `{"keyword":…}` 可用，但库里**没有**极光旧梦 |

## 二、官方三件套（必需的底座）

```
https://modelscope.cn/models/Comfy-Org/Krea-2/resolve/master/diffusion_models/krea2_turbo_int8_convrot.safetensors
https://modelscope.cn/models/Comfy-Org/Krea-2/resolve/master/text_encoders/qwen3vl_4b_fp8_scaled.safetensors
https://modelscope.cn/models/Comfy-Org/Krea-2/resolve/master/vae/qwen_image_vae.safetensors
```

## 三、官方 11 个 LoRA（ModelScope `Comfy-Org/Krea-2/loras/`）

`krea2_darkbrush`、`dotmatrix`、`kidsdrawing`、`neondrip`、`rainywindow`、`retroanime`、`softwatercolor`、`style_reference`（435.9 MB）、`sunsetblur`、`turbo_lora_rank_64_bf16`、`vintagetarot` —— 每个约 447.6 MB。

## 四、社区 LoRA 的两条可行路径

### 路径 A：Civitai 还在架上的 → 直接找 HF 镜像

`https://hf-mirror.com/<org>/<repo>/resolve/main/<path>`

例：`Detailer_Beauty_Krea2`（114 MB）

```
https://hf-mirror.com/RunningHubAI/rh-krea-2-detailer-beauty-for-krea2-lora/resolve/main/Detailer_-_Krea2_project.safetensors
```

### 路径 B：Civitai 已删档的 → civarchive 拿 sha256 → 对 HF 归档库

1. 在 `civarchive.com` 搜模型名，进 `https://civarchive.com/sha256/<sha256>` 页，抄下 `model id` / `version id`。
2. 去 HF 的归档镜像 `k2loras/krea2-lora-archive`，按 `manifest.json` 里的路径翻 `archived_version_ids`。
3. 命中后路径形如：

```
https://hf-mirror.com/k2loras/krea2-lora-archive/resolve/main/2026-07-10/Krea-2/2767709_Krea2-si_-wooupp--Style/3115551/si_(wooupp)_000001000.safetensors
```

实测：极光旧梦（真名 `mhDreamy · Dreamy Cinematic Style (Krea 2) v1.1`，model 2973039 / version 3369293）在归档里**没有**，`civarchive` 的下载按钮最终仍指向 `civitai.com/api/download/models/3369293`，全线不通 → 只能人肉转存。

## 五、人肉转存的落点（Windows 微信）

- 微信客户端在 `D:\Weixin\`，数据根 `D:\xwechat_files\wxid_<你的id>_<后缀>\`。
- 「文件传输助手」收到的普通文件落在 `msg\file\<YYYY-MM>\`，按文件名直接找。
- 拿到的 safetensors 直接改名丢进 `D:\ComfyUI-models\loras\`，**不用重启**：`/object_info/LoraLoaderModelOnly` 立刻能看到。

## 六、确认是否装对

```powershell
# 1) 节点列表里能看见
(Invoke-RestMethod "http://127.0.0.1:8188/object_info/LoraLoaderModelOnly").LoraLoaderModelOnly.input.required.lora_name[0] -match "aurora"
# 2) 读 safetensors 头，看真实来源与设计权重
python -c "import json,struct;f=open(r'D:\ComfyUI-models\loras\<file>.safetensors','rb');n=struct.unpack('<Q',f.read(8))[0];print(json.loads(f.read(n))['__metadata__'])"
```

极光旧梦的实际 metadata：`merged_from_a: krea2_auroraDream2(极光旧梦2)-AURORAL-1.0_3500步`、`merged_from_b: AURORAL_Retro_v3_lr3500`、`method: rank-concat (lossless)`、`note: weight 1.0 = designed strength`。
