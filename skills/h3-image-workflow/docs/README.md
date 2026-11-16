# 参考图工作流 · 零基础使用手册

读者假设：没用过 ComfyUI，也不懂「节点」「latent」这些词。每一节先讲「这是在干什么」，再讲怎么做，最后讲出错怎么查。
版本：2026-11-16 ｜ 对应 skill：`h3-image-workflow` ｜ 实测环境：ComfyUI 0.45.2 + MiniMax H3 int8 + RTX 5060 Laptop 8 GB

---

## 1. 这是什么

ComfyUI 是一个「画流程图来生图」的软件：你把一个个方框（节点）用线连起来，它按顺序执行。
MiniMax H3 是其中一个模型，它有两种用法：

- **纯文字**：你写一段话，它画一张图。
- **参考图**（就是这个 skill）：你给一张图，再写一段话，它画一张「像那张图里的人、但构图不一样」的图。

第二种能锁住一个角色的长相——你今天出了一张满意的，明天还能出同一个人的另一张。
但它有四个坑，不踩过就会反复白跑：脸永远是真人照片、换什么角度都是同一张、报奇怪的错、显存爆掉。

---

## 2. 前置条件（先确认这四件事）

### 2.1 ComfyUI 在跑

在浏览器打开 `http://127.0.0.1:8188`。看到一片深色画布和一堆方框，就是在跑。
打不开 → 桌面上的 ComfyUI 图标点开，等它自己打开浏览器。

**为什么**：后面的每一步都要跟这个「本地服务」说话，它不开，什么都没法做。

### 2.2 模型在

在 ComfyUI 里点左上角菜单 → 找 `models` 目录，确认有这些文件：

| 类型 | 文件名（必须完全一致） |
|---|---|
| diffusion_models | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` |
| text_encoders | `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` |
| vae | `minimax_h3_video_vae_fp16.safetensors` |

没有 → 先把文件放进对应目录（一般在 `C:\Users\你的用户名\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models\` 下），重启 ComfyUI。

### 2.3 参考图在 `input` 目录

把参考照片复制到 `...\ComfyUI-Shared\input\`（记住文件名，比如 `ref.png`）。

**为什么**：`LoadImage` 这个节点只认 `input` 目录里的文件，不是随便哪里都能读。

### 2.4 显存够

8 GB 可以跑 768×1344，一张 2–3 分钟。低于 6 GB 会中断。

---

## 3. 分步操作

### 3.1 你只需要改三个地方

如果你拿到的是现成工作流（`.json`），拖进 ComfyUI 画布，然后只改：

1. `LoadImage` 里的照片（换成你的参考图）；
2. `MiniMaxH3ImageConditioning` 里的提示词（换成你要的画面）；
3. `RandomNoise` 里的种子（想换一张就 +1）。

### 3.2 三个关键开关（这是全篇最重要的一段）

| 开关 | 在哪 | 什么时候要动 |
|---|---|---|
| **接不接 vae** | `MiniMaxH3ImageConditioning` 的 `vae` 输入 | 想要 CG 质感 → 断开；想要照片质感 → 接上 |
| **接不接 images** | 同一个节点的 `images` 插槽 | 想换机位（俯拍、侧面、背后）→ 断开；只换景别以内 → 接上 |
| **宽高** | 同一个节点的 `width/height` | 永远写死 768 / 1344，不要留 0 |

**为什么**：
- vae 接上时，参考图会被压成一份「画面底稿」塞进模型，权重很大，文字说破天也改不动它——所以脸一直是真人。
- images 接上时，参考图的构图（机位、左右位置、人物大小）也会一起被复制——所以你怎么写「俯拍」都还是原图那个角度。
- 宽高留 0 时，程序按参考图的短边自动算画布，9:16 会算出约 180 万像素，8 GB 显存扛不住。

### 3.3 用 API 提交（不开界面也能跑）

界面上连好线后，点右上角 `Save`，再用下面这行命令提交（PowerShell）：

```powershell
# 把 workflow_api.json 换成你导出的文件名；导出时要选「Export (API)」
$json = Get-Content "workflow_api.json" -Raw -Encoding UTF8
Invoke-RestMethod "http://127.0.0.1:8188/prompt" -Method Post -Body $json -ContentType "application/json"
```

返回一个 `prompt_id` → 用 `http://127.0.0.1:8188/history/<prompt_id>` 查结果，
出图在 `...\ComfyUI-Shared\output\` 下，文件名前缀由 `SaveImage` 节点决定。

---

## 4. 为什么这么设计（理解了三分钟就够）

模型干活分四步：**读提示词 → 造一张噪点底图 → 一步步去噪 → 解码成图片**。

- 「读提示词」这一步，参考图可以走两条路：走 vae（当成画面底稿，权重最大）或只走文字编码器（只当形容词）。
- 「造底图」这一步的尺寸必须由你定，不然它自己按参考图算。
- 「去噪」的步数决定细节多少：30 步能出布料纹理和光斑，6 步只有大概形状。
- 「解码」永远要用 vae，所以就算你把参考图的 vae 断了，解码那个 vae 不能断——这是最容易误删的地方。

---

## 5. 报错对照表

| 你看到的 | 意思 | 怎么办 |
|---|---|---|
| `execute() got an unexpected keyword argument 'image_0'` | API 里那个插槽的名字少写了 `images.` 前缀 | 改成 `"images.image_0": ["7", 0]` |
| `Required input is missing: images` | 删键时删多了或拼错 | 只删 `images.image_0` 这一行 |
| `CUDA out of memory` | 画布太大 | 宽高改成 768 / 1344；关掉别的占显卡软件 |
| 图片全黑 / 全灰 | vae 接错节点 | `VAEDecode` 的 vae 必须接 |
| 出图和参考图一模一样 | 提示词里写了 same close crop | 写明新的景别与机位 |
| 换机位没用 | images 插槽还连着 | 断开 `images.image_0` |
| 永远是真人脸 | vae 还连着 | 断开 `MiniMaxH3ImageConditioning` 的 vae |

---

## 6. 怎么算成功

跑完先看这四条，全中才算成：

1. **脸是同一张**：把新图和参考图并排，五官位置、眼距、下颌线一致。
2. **机位是新的**：俯拍就是俯拍，侧面就是侧面，不是原图角度换了张皮。
3. **质感对**：要 CG 就是瓷面、发片分明、没有毛孔；要照片就是有颗粒和皮肤纹理。
4. **没有多余手指 / 第二个人 / 乱码文字**。

任何一条不中 → 打开 [../references/failure-table.md](../references/failure-table.md)，按「症状」那一列找。

---

## 7. 术语表

| 词 | 人话 |
|---|---|
| 节点（node） | 画布上的一个方框，干一件事 |
| 工作流 | 一堆连好线的节点，存成 `.json` |
| API 格式 | 给程序看的 JSON，跟界面里的连线是同一回事 |
| latent | 模型内部用的「半成品图」，还不是真正的图片 |
| vae | 把半成品翻译成图片的翻译官 |
| 种子（seed） | 随机数起点；同种子同参数 = 同一张图 |
| 步数（steps） | 去噪迭代多少次，越多越细 |
| autogrow 插槽 | 能无限加插槽的输入（这里指「可以塞很多张参考图」） |
| 蒸馏 / HyperFlow | 把 30 步压成 6 步的加速版，快但细节少 |

---

## 8. 版本与变更

| 日期 | 变更 | 验证 |
|---|---|---|
| 2026-11-16 | 初版：四种配方、api-graph 骨架、12 条失败对照 | 本机实测 20+ 张，152–185 s/张 |
