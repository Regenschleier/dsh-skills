# 更新记录

## 2026-11-17

**二次检验（2026-11-17，按「写入正文必须二次检验」的新要求重审）**

- `character-design/SKILL.md`：给尚未验证的说法加标注——第八节说明本机只验证过单幅人像与景别锚点；第十节第 2 条（多视图换脸）标明「本机未做对照，属推断」；第十二节平台差异表逐行区分「实测 / 推断 / 未做对照」。
- `references/framing-lock.md`：换算表标注只有前三行直接验证过，「半身 / 特写」两行为原理延伸、未单独实测；复现命令改指向真实存在的 `h3-image-workflow/references/api-graph.md`（原来写的相对路径是错的）。

**character-design：补「景别与全身锁定」，并按审核结论改口**

- 新增 `references/framing-lock.md`：把「镜头口令」与「画面位置锚点」两种写法的实测对照整理成表（含 seed），给出换算表与出图后 3 秒自检。
- `SKILL.md` 新增四节：八 产出分发 / 九 景别与全身锁定 / 十 身份锚点与「看不见的地方」 / 十一 多视图资产图（标注「本机未实测」）/ 十二 平台差异表（MJ 与本机的可移植项）。
- 新增 `examples/` 对照图两张：`failure-05-body-lock-words-cropped.jpg`、`success-06-frame-anchors-full-body.jpg`（人脸已模糊处理），配 `examples/README.md` 说明来历。

**审核改口（重要）**：初版把结论写成「镜头口令一定失效」。复测后修正为——带参考图时口令容易被构图钉死（同一主体三个 seed 都裁到小腿），位置锚点一次到位；不带参考图时口令也能出全身。文档按这个分寸重写，不夸大。

## 2026-11-16

**新增 skill：`character-design`**

- `SKILL.md`：判断表（CG / 照片 / 纪实 / 视频）、三条硬开关（参考图 vae、images 插槽钉构图、动作段要重写）、八段骨架、已定版的渲染锚、反恐怖谷四条、参考图分工、自检清单。
- `references/prompt-skeleton.md`：八段中英对照填空模板，附「暗调莫兰迪」变体的渲染锚替换写法。
- `references/failure-table.md`：12 条「症状 → 病因 → 改哪段」对照。
- `docs/README.md`：零基础手册（八节：这是什么 / 前置条件 / 分步操作 / 为什么 / 报错对照 / 怎么算成功 / 术语表 / 日期版本）。

**新增 skill：`h3-image-workflow`**

- `SKILL.md`：四条硬开关（images 钉构图 / vae 定照片或 CG / 宽高写死 / 动作段要重写）、节点接线图、四种配方对照（锁身份换机位、只锁渲染语言、照片翻 CG、纯文字）、参考图准备规则、参数表、自检清单。
- `references/api-graph.md`：可直接 POST 的 API JSON 骨架，含「只删一行就是 CG」「再删一个键就是换机位」两种改法。
- `references/reference-prep.md`：CG 进 CG 出、裁比例、两种「锁」的写法、防对称化。
- `references/failure-table.md`：12 条症状对照 + 30 秒定位顺序。
- `docs/README.md`：零基础手册（八节，含「三个关键开关」图解式说明与 API 提交方法）。

验证环境：ComfyUI 0.45.2、MiniMax H3 int8 fl2va、30 步、768×1344、RTX 5060 Laptop 8 GB、Windows。
实测耗时：纯文字 105 s／张，带参考图 152–185 s／张。

已知限制：反恐怖谷四条只在本机这三套权重上验证过，换模型需重测；`h3-image-workflow` 的机型覆盖只有 RTX 5060 Laptop 8 GB。

### 修订：`h3-image-workflow` 审核后改掉的四处（2026-11-16 第二次提交）

按「先审核再发布」重审第一版，找出四处不合格并已修：

1. **接线图里多了一个 `CLIPTextEncode`**（写着「想更强就再喂一次」）——参考图链路根本不走它，提示词直接写在节点 6 的 `prompt` 里。已删，并加了一句区分两种链路。
2. **API 提交缺一层包装**——界面导出的裸节点表直接 POST 会被拒，必须包成 `{"prompt": {...}}`。旧版手册照抄会直接失败。已给出完整 PowerShell 与说明。
3. **报错表里有两行是编的**（`Required input is missing: images`）——没实测过就写进了对照表。已删，留下的每行都标了「实测 / 推断」。
4. **「拖进画布就行」是没验证的说法**——API 格式的 JSON 能否拖进 ComfyUI 画布我没验证过，已改成明确说明。

新增 `examples/`：9 张实拍对照图（5 成功 4 失败），每张下面写清配置、症状、病因与改法。

