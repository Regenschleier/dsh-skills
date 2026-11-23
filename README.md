# dsh-skills

给 DeepSeek Harness（DSH）用的 skill 集合。每个 skill 是一段写好的、可复用的操作手册：模型照它做事，人照它排查。

## 目录

| skill | 一句话 | 文档 |
|---|---|---|
| `character-design` | 把「想要这种感觉」翻译成可复现的人像提示词，产出半写实 3D CG 日系少女 | [SKILL.md](skills/character-design/SKILL.md) ｜ [零基础手册](skills/character-design/docs/README.md) |
| `h3-image-workflow` | 把 MiniMax H3 的「参考图 → 新图」接对：锁身份、换机位、照片翻 CG，以及那个会让构图钉死的坑 | [SKILL.md](skills/h3-image-workflow/SKILL.md) ｜ [零基础手册](skills/h3-image-workflow/docs/README.md) |
| `krea2-local` | 在本机 ComfyUI 跑 Krea 2 Turbo（int8），用 STYLE 措辞定画风、用 LoRA 叠电影感，并知道什么强度会翻车 | [SKILL.md](skills/krea2-local/SKILL.md) |
| `live-wallpaper` | 把一张静图做成可导入 Wallpaper Engine 的无缝循环 4K 动态壁纸（程序化 2.5D 运镜 + PyAV 编码） | [SKILL.md](skills/live-wallpaper/SKILL.md) ｜ [推导与数据](skills/live-wallpaper/references/motion-and-composition.md) |

## 怎么用

**给 DSH 用**：把 `skills/<名字>/` 整个目录放进下面任意一个位置，DSH 会自动发现（不用重启）：

- 项目内：`<你的项目>/.dsh/skills/`
- 项目内（通用）：`<你的项目>/.agents/skills/`
- 全局：`%USERPROFILE%\.dsh\skills\`

目录里必须有 `SKILL.md`，开头是 `---` 包起来的几个字段（`name`、`description`），DSH 靠 `description` 判断什么时候该用它。

**给自己看**：每个 skill 的 `docs/` 下是一份零基础手册——每一节先说「这是在干什么」，再说怎么做。不需要懂提示词，也不需要懂 ComfyUI。

## 写作约定

1. 每个 skill 的 `SKILL.md` 只写**给模型看的操作规则**（判断、顺序、阈值、红线）。
2. 人看的说明书放 `docs/`，按八节写：这是什么 / 前置条件 / 分步操作 / 为什么 / 报错对照 / 怎么算成功 / 术语表 / 日期版本。
3. 每一步都要回答三个问题：**在干什么、为什么、失败怎么查**。
4. 不写没验证过的结论；写了的，注明验证日期与环境。

## 版本

见 [CHANGELOG.md](CHANGELOG.md)。