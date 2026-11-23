---
name: krea2-local
description: 在本机 ComfyUI 上跑 Krea 2 Turbo（int8）出图，并叠多个 Krea2 LoRA 把「半写实 CG」做成电影感：模型三件套、8 步参数、UI 工作流怎么摆、LoRA 叠几层、每层多少权重、什么时候会翻车。用户说「用 krea2 出图 / 加个 LoRA / 这组风格不对 / 多来几个视角」时用它。
---

# Krea 2 Turbo（本地 int8）出图与 LoRA 叠加

这份手册只讲**本机已验证**的链路：ComfyUI 本地后端 + `krea2_turbo_int8_convrot` + Qwen3-VL 文本编码器 + Qwen-Image VAE。云端 `Krea2StyleReferenceNode` 是另一条链路，权限和结果都不一样，见第五节。

## 一、先记住三件事

1. **画风由 STYLE 段的措辞决定，不由 LoRA 决定。** 同一个 seed、同一个提示词，只把 STYLE 段从「painterly anime render」换成「semi-realistic 3D character render, subsurface-scattering skin, individually modelled hair strands…」，出图直接从扁平插画变半写实 CG（2026-11-23 实测，`krea2_style_reference` 权重 0.9 与 0.0 两张质地几乎一致）。
2. **LoRA 是「调味」，不是「开关」。** 主风格 LoRA ≤1.0、细节 LoRA 0.5–0.7、小风格 0.3–0.5，**总强度预算 2.0–2.3**；超过就换角色。
3. **风格越重，构图越不听话。** 过载档（1.6/1.3/1.0）连试三次都拍不出全身，只能出近景/半身；要全身就降到 1.0/0.7/0.4。

## 二、三件套与固定参数

| 项 | 值 | 存放位置 |
|---|---|---|
| UNET | `krea2_turbo_int8_convrot.safetensors`（12.57 GB） | `models\diffusion_models\` |
| CLIP | `qwen3vl_4b_fp8_scaled.safetensors`，`type=krea2`、`device=default` | `models\text_encoders\` |
| VAE | `qwen_image_vae.safetensors` | `models\vae\` |

采样固定：**8 步 / cfg 1.0 / euler / simple / denoise 1.0**。832×1248 单张约 25–45 秒（8 GB 显存 laptop，int8）。

加载顺序（模型链）：`UNETLoader → LoraLoaderModelOnly(style_reference 0.9) → LoraLoaderModelOnly(主风格) → LoraLoaderModelOnly(细节) → KSampler`。每个 LoRA 节点只吃上一层的 `model` 输出，别把 UNET 直接连 KSampler 又连 LoRA。

## 三、提示词的三段式

```
STYLE 段   —— 决定介质（写死在最前）
LOOK 段    —— 角色的固定外观，逐条列（发色/发型/眼/斑点/帽子/外套/包带）
SCENE 段   —— 这一张的机位、动作、光、景
NEG 段     —— 只放真正要压掉的东西
```

- **STYLE 段是画风开关**，不要和 SCENE 混写。半写实 CG 的已验证写法：

  ```
  Semi-realistic 3D character render, like a frame from a Japanese CG animated film:
  subsurface-scattering skin, individually modelled hair strands, cloth with real thickness
  and weave, soft cinematic light with a cool rim, gentle depth of field, fine film grain.
  Not a line drawing, no cel shading, no flat colour blocks, no outlines.
  ```

- **LOOK 段要写「成年人比例」**：不写 `adult proportions / roughly eight heads tall` 并加负面 `chibi, child proportions, big head, short legs`，全身镜头会出成三头身。
- **SCENE 段写「画面位置」而不是镜头焦距**：`her whole figure from beanie to boots fits inside the frame, head near the top fifth, boots touching the bottom fifth`。写 `85mm`、`further back` 这类摄影词在这条链上基本不生效。

## 四、LoRA 叠加（详见 `references/lora-stacking.md`）

档位记法：`style_reference 0.9 / 主风格 X / 细节 Y / 小风格 Z`。

| 档 | 权重 | 结果 | 用途 |
|---|---|---|---|
| 轻 | 1.0 / 0.7 / 0.4 | 接近原始 CG，能拍全身 | 全景、全身、要保角色设定 |
| 重（过载） | 1.6 / 1.3 / 1.0 | 电影级逆光、金属扣、毛领全出，但**会自动加设定外细节**、脸会变尖 | 近景、半身、封面 |
| 单层 | 主风格 1.0 其余 0 | 只加调色与金边，不抢角色 | 大场景、多人 |

三条硬规则：
1. 叠之前先单独跑一遍新 LoRA（同 seed、`off` 对照），确认它到底加什么——`Detailer_Beauty_Krea2` 实际是「美颜」，不是「加细节」。
2. 主风格 1.4 以上开始自作加饰物；1.6 已在换脸边缘。
3. 滑块类 LoRA（brightness/light slider）全场只留一个，否则互相抵消。

## 五、本地 vs 云：两条链路，别混

| | 本地 int8 | 云端 `Krea2StyleReferenceNode` / `Krea2ImageNode` |
|---|---|---|
| 权限 | 无需登录 | **必须**在 ComfyUI 桌面端登录 Comfy 账号，否则 `Unauthorized: Please login first to use this node.` |
| 参考图 | 走 CLIP 视觉 token，锁构图与介质 | 上传到 ComfyAPI 存储，当 URL 传给模型 |
| 默认画风 | 纯文字容易落回动漫插画 | 更接近用户在外面看到的「半写实 3D」 |
| 成本 | 本地算力 | 走 Comfy 额度 |

用户说「怎么变画风了」时，先问清那张是本地还是云出的——两边同 seed 同提示词也不是一个东西。

## 六、UI 工作流的两个坑

1. **工作流必须放服务器真正的 user 目录**：`ComfyUI-Installs\ComfyUI\ComfyUI\user\default\workflows\`。放 `ComfyUI-Shared\user\default\workflows\` 会 404（`/api/userdata?dir=workflows` 返回 `[]`）。
2. **手写 UI 格式 JSON 时，links 表要先分配 id 再回填** `inputs.link` / `outputs.links`；用 `lid - N` 这类算术会错位（实测抓到 7 处错连）。写完用 `app.loadGraphData(data)` 载入 + 读 `graph._nodes` 的连线数自检，再点运行。

## 七、模型从哪来（详见 `references/model-sources.md`）

- 官方 11 个 Krea2 LoRA：ModelScope `Comfy-Org/Krea-2/loras/`（每个约 447 MB，含 darkbrush / neondrip / retroanime / softwatercolor / style_reference 等）。
- 社区 LoRA：`hf-mirror.com` 可直连；Civitai 删档的模型可经 `civarchive.com` 找到 sha256 → 再对上 HF 的 `k2loras/krea2-lora-archive` 镜像路径。
- `seaart.ai` / `tensor.art` / `civitai.com` 本机不可直连，模型页打开即超时；这两家的独占 LoRA 只能靠人肉转存（微信文件传输助手最快）。

## 八、交付检查

出完图先自问四句：
1. 角色还是她吗（脸型、发色、眼睛没被 LoRA 改掉）？
2. 我写的构图（全身 / 半身 / 侧面）真的成立吗？
3. 有没有多出来的饰物、文字、水印？
4. 介质对不对（要 CG 就不要出成插画，要插画就不要出成真人）？

四条里有任何一条不对，先降强度再改措辞，不要靠加排除项硬压。
