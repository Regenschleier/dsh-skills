# 更新记录

## 2026-11-19

**更正：背面朝向可以由措辞救回来（A/B + 重复验证，seed 20264001–20264003）**

- 之前 `references/multi-view-orientation.md` 写的「朝向只能靠换参考图、措辞压不住」**说得太绝，已改口**。
- 新对照：同一张**正面** 2D 角色卡，句尾塞 `her back to the lens` 且照写五官 → 3 个 seed（20261903/04/05）全出正面；改成**句首**写 `The camera stands behind her: we see the back of her head and the back of her cape` + **全篇不写脸** → 3 个 seed（20264001/02/03）全出对背身。
- 顺带 A/B：同 seed 20264001，A 不加排除项、B 加满 `no front view, no face, no eyes, no side view, no three-quarter view`，**两版都出对、看不出差别** ⇒ 排除项在这条上不是关键变量，因此没有把 MJ 那串排除项写进推荐做法。
- 同步更新 `SKILL.md` 第十一节摘要、`examples/README.md` 新增一节对照（内嵌 `failure-08` 与新的 `success-11-back-view-by-wording.jpg`），并把该页拼版尺寸由 1344×768 更正为 2304×1344、示例代码同步改。

## 2026-11-18

**三视图的媒介由参考图决定（2D 进 2D 出 / 3D 进 3D 出）**

- `character-design/SKILL.md` 第十一节新增小节「媒介由参考图决定，加形容词改不动」，并附「参考图 → 骨架怎么写」对照表。
- 依据全是本机实测：2D 平涂角色卡（崩坏 / Thelema）即使把开头写成 `3D CG character reference sheet`、把 CG 锚提到第一句、甚至断开 conditioning 的 vae（seed 20261201 / 20261202 / 20261211 三次），出来的仍是平涂线稿；真人照片参考出来就是照片（20261116 / 20261117）；3D 渲图的裁切出来是半写实 CG（20261171）；2D 立绘 + 明确写 cel-shaded 出 2D 立绘（20264001）。
- 结论与「朝向由参考图决定」同一机制：**要 2D 就别塞 CG 词，要 CG 就换 3D 渲过的参考图（或撤掉参考图纯文字写）**。

**三视图「眼睛没了」：分辨率与措辞的对照（seed 20264001）**

- `references/framing-lock.md` 新增一节「三视图/角色表：脸被压到多少像素」：算出 1344×768 塞三列时每列只有 448 px、头约 110 px、眼睛约 10 px，放大 6 倍就是两团暗红影子；改成每视角单图 768×1344 再拼成 2304×1344 后，头约 200 px、眼睛约 25 px，眼白/虹膜/瞳孔/高光都读得出。附推荐做法（三张单图 → PIL 横拼 → 再降采样交付）。
- 同节记录了措辞教训：照抄原画设定的 `narrow red eyes` 会画出细缝，改成写明 sclera / iris / pupil / specular 才有眼睛；并**明确标注这是推断**——分辨率与措辞同时改，单项作用未做隔离实验。
- 新增案例图 `failure-10-eyes-lost-at-448px.jpg`、`success-10-eyes-readable-2304-sheet.jpg`，`examples/README.md` 加一节对照说明。

**修好 examples/README.md 里四个失效的图片路径**

- 该文件本身就在 `examples/` 目录里，原来写成 `../failure-08-….jpg` 会指到 `character-design/` 下，页面显示破图；已改为 `failure-08-….jpg`（相对同目录）。同时把本轮两张新图也按同目录写法接上。

## 2026-11-17

**三视图实测（2026-11-17）**

- `character-design/SKILL.md` 第十一节由「本机未验证」改为实测结论：1344×768 横排三列 + 画面位置锚点，三次跑都出对了版式；补了三条已知偏差（特写列过大、胸甲读成光滑壳、背面被大衣遮住）。
- `examples/success-07-three-view-turnaround.jpg` 新增，配 `examples/README.md` 条目（seed 20261301，另两次 20261302 / 20261311 同结构）。

**二次检验（2026-11-17，按「写入正文必须二次检验」的新要求重审）**

- `character-design/SKILL.md`：给尚未验证的说法加标注——第八节说明本机只验证过单幅人像与景别锚点；第十节第 2 条（多视图换脸）标明「已验证一半：一份描述跑三视图是同一角色；只写 the same character 的对照组未跑」；第十二节平台差异表逐行区分「实测 / 推断 / 未做对照」。
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


**三视图的「朝向」与「部件」专项（2026-11-17 追加）**

新增 character-design/references/multi-view-orientation.md，把后视图最容易翻车的地方单独成页，十条对照全部带 seed：

- 朝向由参考图决定，不由措辞决定：正面参考图 + 「camera stands BEHIND her / no eyes, no nose, no mouth」写到最后一次仍出正面（seed 20261903 / 20261904 / 20261905）；换成紧裁切的背面参考图，一次出对（20261910）。
- 部件也会被参考图带错：背面参考图里是短靴，提示词写「及膝长靴」仍出短靴（20262003）。
- 解法是双参考图：images.image_0 管朝向、images.image_1 管部件特写，提示词分两段写 <Picture 1> / <Picture 2>（20262041，朝向与靴子同时对）。
- 跨列一致性靠措辞不稳（把「背面头发到腰」写进服装段反而把大衣拆碎，20261511；挪进版式锚点命中，20261521；同句换回 b 版 seed 20261522 又失败），稳定解是每列单图再 PIL 拼版。
- 附带四条易错点与出图前 5 秒自检清单；第五节给了可直接运行的 PIL 拼版代码。

新增案例图 4 张（均本项目自渲染，640 宽 JPEG q84）：ailure-08-back-words-still-front.jpg、ailure-09-back-wrong-boots.jpg、success-08-back-from-back-reference.jpg、success-09-back-boots-two-refs.jpg，并在 examples/README.md 逐张说明「怎么来的、为什么算成/算败」。

SKILL.md 第十一节末尾加了指向该页的四句摘要，方便不点进 reference 也能抓住要点。
