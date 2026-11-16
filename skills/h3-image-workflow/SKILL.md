---
name: h3-image-workflow
description: 在 ComfyUI 上把 MiniMax H3 的「参考图 → 新图」工作流接对、跑稳：MiniMaxH3ImageConditioning 的接线、images.image_0 这个带点键的坑、vae 接不接决定照片还是 CG、换机位为什么永远失败。当需要锁住一个已定版角色、把照片翻成 CG、或换机位/换景别重出图时使用。
whenToUse: 已有满意的成图或参考照片，要求「照这个角色再做几张」「换个角度」「换身衣服但脸别变」；或工作流报 execute() got an unexpected keyword argument。
---

# H3 参考图工作流（MiniMaxH3ImageConditioning）

## 这个 skill 解决什么

ComfyUI 里的 MiniMax H3 有两个入口：纯文字（`CLIPTextEncode` 直接喂 `BasicGuider`）和参考图（`MiniMaxH3ImageConditioning`）。
参考图入口能锁身份，但有四个坑，不踩过就会得到「脸永远是真人照片」「换哪个角度都是同一张」「报 TypeError」。
本 skill 给出可复制的接线、四种已验证配方、以及每个现象对应的改法。

## 一、四条硬开关（按重要性排序）

1. **`images` 插槽接着参考图，构图就被钉死。** 写「俯拍 / 背后 / 特写」出来还是原图那个机位。换机位必须把整个 autogrow 插槽删掉，人物改用文字重写。
2. **接不接 `vae` 决定「照片」还是「CG」。** 接着 vae → 参考图被编码成 `minimax_refs` latent，权重压过文字，脸会一直是真人五官；断开 vae（`VAEDecode` 那根照接）→ 参考图只进文本编码器，画面跟提示词走，立刻变瓷面 CG。
3. **宽高写死，别留 0。** `width/height` 默认 0 时会按参考图短边 1024 自动出画布（9:16 约 1.8 MP），8 GB 显存会爆或极慢；一律显式 `768×1344`。
4. **换机位时动作段必须整段重写。** 残留 `stomp / kick / sneaker the largest` 这类上一张的词，会把机位拉回原构图。

## 二、接线（API 格式，照这个连）

```
UNETLoader(int8 fl2va) → ModelAttentionBackend("comfy kitchen attention")
        ├── BasicGuider(model)          ← conditioning 来自节点 6 的第 0 输出
        └── BasicScheduler(simple, 30, 1)
CLIPLoader(qwen3vl_32b, minimax) ──┬── CLIPTextEncode(prompt)   ← 想更强就再喂一次
                                   └── 节点6.clip
VAELoader(minimax_h3_video_vae_fp16) ─┬── 节点6.vae   ← 想出 CG 就把这根删掉
                                      └── VAEDecode.vae
LoadImage → 节点6["images.image_0"]
节点6.latent(第1输出) → SamplerCustomAdvanced.latent_image
SamplerCustomAdvanced(noise, guider, KSamplerSelect(res_multistep), sigmas)
        → LTXVSeparateAVLatent(av_latent) → 取第 0 输出 video_latent → VAEDecode → SaveImage
```

可复制的 JSON 骨架见 [references/api-graph.md](references/api-graph.md)。

**最常踩的语法坑**：autogrow 插槽在 API 里是**带点的字面键** `"images.image_0": ["7", 0]`。
写成 `"image_0"` 会当关键字参数传给 `execute()`，报
`MiniMaxH3ImageConditioning.execute() got an unexpected keyword argument 'image_0'. Did you mean 'images'?`

## 三、四种配方（选一个，别混）

| 目标 | vae | images | 提示词重心 |
|---|---|---|---|
| 锁身份、换机位 | 接 | **删掉** | 人物写文字 + `<Picture 1>` 完全不提 |
| 锁身份、只换景别以内 | 接 | 接 | 开头写 `<Picture 1> teaches only the rendering language and the face` |
| 照片 → CG（保骨相） | **断开** | 接 | CG 渲染锚 + 景别「改写成腰以上四分三侧」 |
| 纯文字出图 | 不需要 | 不需要 | 全套八段文字 |

选错一条的表现：想换机位却仍接着 images → 四张图同一构图；想 CG 却接着 vae → 永远是真人照片。

## 四、参考图怎么准备（决定成败的一半）

- **CG 进 CG 出最稳**：想要 CG 新图，就用已认可的 CG 成图裁一份当参考，比用手机照片稳得多。
- 要保构图就**裁成目标比例**（9:16）再喂，否则模型会把原图机位一起搬过来（低机位仰头怼脸的照片会带来难看的下颌）。
- 参考图只承担「骨相 / 服装 / 材质」，别指望它承担新机位——机位永远写在文字里。
- 细节会对称化：单侧颜料痕、单侧耳钉这类，要单开一段点名「另一侧干净」。

模板见 [references/reference-prep.md](references/reference-prep.md)。

## 五、参数（8 GB 笔记本实测）

| 项 | 值 | 备注 |
|---|---|---|
| 尺寸 | 768×1344 | 32 的倍数，总像素 ≤ 768×1344 |
| 步数 | 30（simple 调度） | 6 步 HyperFlow 会抹掉材质与光斑，只适合草稿 |
| 采样器 | res_multistep | 模板默认；euler 也可 |
| 注意力后端 | comfy kitchen attention | int8 专用，N 卡 |
| 耗时 | 纯文字 105 s；带参考图 150–185 s | RTX 5060 Laptop |

## 六、失败对照表（症状 → 病因 → 改哪）

完整 12 条见 [references/failure-table.md](references/failure-table.md)。最常见的四条：

| 症状 | 病因 | 改法 |
|---|---|---|
| 四张不同机位的图长得一样 | images 还接着参考图 | 删 `images.image_0`，人物文字重写 |
| 永远是真人照片 | 节点 6 接着 vae | 断开 vae（VAEDecode 照接） |
| 报 TypeError: unexpected keyword argument | autogrow 键写成 `image_0` | 改成 `images.image_0` |
| 换机位后回到旧动作 | 提示词残留上一张的动作词 | 动作段整段重写 |

## 七、自检（提交前 20 秒）

1. 我要「换机位」还是「只换景别」？换机位 → images 必须为空。
2. 我要「CG」还是「照片」？CG → 节点 6 不接 vae。
3. 宽高是不是 768×1344（不是 0）。
4. 提示词里有没有残留的上一张动作词。
5. 参考图比例是否与目标比例一致。

## 八、和视频的衔接

静帧定版后再接 `MiniMaxH3ImageToVideo`：把定版图当 `first_frame`，`length` 用 124（24 fps，约 5 s），
提示词改成时间码分段（`[0.0s-1.5s] …`），镜头动作写成画面占比变化而不是厘米数。
在蒸馏版（HyperFlow 6 步）上，雾、颗粒、光晕会被抹掉，要写成「欠半档、全画面发雾、不锐」这种可判定状态，或干脆后期加。
