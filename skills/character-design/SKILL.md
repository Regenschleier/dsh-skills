---
name: character-design
description: 在 ComfyUI + MiniMax H3 上把一句「想要这种感觉」翻译成能出图的提示词与工作流，产出用户认可的半写实 3D CG 日系少女。当任务涉及写人像提示词、调参考图、换机位、修「诡异」「太丑」「画风变了」这类问题，或需要复用已定版配方时使用。
whenToUse: 用户要生成/改人物图，或在别处复现同一套人像观感；或拿着参考照片要求「照这个感觉做一套」。
---

# 角色设计（半写实 3D CG 人像）

## 这个 skill 解决什么

把「好看」这种说不清的要求，变成可判定、可复现的提示词段落，并且知道哪一段坏了该改哪一段。
本机已验证的链路：ComfyUI 0.45.x + MiniMax H3（int8 fl2va，30 步）+ 可选参考图。

## 一、先判断用户要哪一种（错一种就白跑）

| 用户说法 | 真实目标 | 配方 |
|---|---|---|
| 「2.5D 日系少女」「动漫脸」 | 半写实 3D CG，允许大眼、瓷面 | 纯文字 + CG 措辞（见第四节） |
| 「照这张照片的感觉」 | 保照片里的人，但翻成 CG 质感 | 参考图（带 vae）+ CG 措辞 |
| 「照片风」「纪实」「莫兰迪」 | 有胶片感的暗调人像 | 参考图可留可去，但**删掉瓷面词**，加介质与调色段 |
| 「动起来」「做成视频」 | 视频 | 先出静帧并让用户点头，再谈视频 |

**判定信号**：只要提示词里同时出现「porcelain / 无毛孔」和「film grain / 纪实」，模型会二选一，通常是恐怖谷。二者只能留一个。

## 二、三条硬开关（不知道就会反复白跑）

1. **参考图节点接不接 vae，决定「照片」还是「CG」**。接 vae → 参考图被锚成 latent reference，权重压过文字，脸会一直是真人；断开 vae（VAEDecode 那根照接）→ 参考图只走文本编码器，画面跟提示词走。
2. **只要 `images` 插槽还接着参考图，构图就被钉死**。写俯拍、背后、特写都会回到原图机位。换机位必须把 images 整个删掉（API 里删 `images.image_0` 这个**带点**的键），人物改用文字重写。
3. **换机位时动作段必须整段重写**。残留 `stomp / kick / sneaker the largest` 这类词会把机位拉回原构图。

## 三、八段骨架（顺序固定，缺段会漂）

人物 → 服装 → 景别与动作 → 光 → 配色 → 镜头与景深 → 构图气质 → 禁止项。
每段写「可判定的状态」，不写物理量（「推近 12cm」在蒸馏模型上无效，写「头像占画幅从 55% 变 65%」）。
落到提示词里还要在前面加一段**渲染锚**（是什么介质），在最后加**隐式负向**（不要什么）。

模板见 [references/prompt-skeleton.md](references/prompt-skeleton.md)。

## 四、已定版的渲染锚（照抄，别改写）

```
A still from a Japanese 3D animated feature film, a CG-rendered character with
semi-realistic materials, never a photograph of a real person and never flat
two-dimensional anime artwork.
```
皮肤：`smooth porcelain CG shader, an even cream-to-peach gradient, no pores, no photographic grain`
头发：`broad semi-transparent hair cards clumping into heavy locks whose rims burn out to white`
眼睛：`eyes a little larger than life, one clean specular highlight, small refined nose, small glossy mouth, clean jawline`
收尾：`filmic tonemapping, gentle highlight rolloff, faint chromatic fringing`

**要成年感**：单独一句写年龄与骨相（`a woman of about twenty-two, an adult, slim neck, defined jaw, chin to a soft point`）。只写「mature / delicate / narrow-lidded」会整体塌成平涂动漫。

## 五、反恐怖谷四条（用户说「诡异」时逐条对）

1. 皮肤从「瓷」改成「瓷但有活气」：`soft and airbrushed but alive`、额头一点油光、血色在皮下；删掉 `glassy / no pores`。
2. 眼神给理由：写 `mid-thought` 并给具体动作（正在合上杯盖、正要笑），不要「凝视画外」。
3. 光给温度：环境冷、人暖（`grey falls on the room, warm falls on her`）；删「她是唯一的光」这种空镜配方。
4. 显式禁止：`no blank stare, no porcelain mask, no glass eyes, no grey corpse light`。

## 六、参考图分工（不要让它同时干两件事）

- 参考图负责**骨相**（成年脸、脸的立体度）；
- 文字负责**材质**（瓷面、发片）与**景别**；
- 「景别与动作」那一段是「复刻 vs 换机位」的开关：写 `same close crop` 就是复刻，改写成 `waist-up, three-quarter, head turned 20° toward the window` 才是换构图。

## 七、自检清单（出图前逐条打勾）

- [ ] 渲染锚在第一段，且没有和介质冲突的词（grain / 纪实 / 手机拍摄）。
- [ ] 年龄与骨相单独一句，没被「delicate」这类词带成幼态。
- [ ] 八段齐，且每段都有可判定的量（占比、光比、机位角度、焦距、景深）。
- [ ] 换机位时 images 已删、动作段已重写。
- [ ] 禁止项写了文字水印、多余手指、第二个人。
- [ ] 尺寸 768×1344（32 的倍数），30 步，int8 权重。

## 八、坏了怎么修

症状 → 病因 → 改哪一段，见 [references/failure-table.md](references/failure-table.md)。
零基础逐步操作（含每一步在干什么、为什么、失败怎么查）见 [docs/README.md](docs/README.md)。
