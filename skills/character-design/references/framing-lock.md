# 景别与全身锁定（H3 实测）

> 证据等级：本文两种写法都是在同一台机器、同一套渲染锚下跑出来的对照（MiniMax H3 int8 fl2va，768×1344，30 步，
> 采样器 res_multistep，conditioning 节点不接 vae）。
> 对照图：`examples/failure-05-body-lock-words-cropped.jpg`、`examples/success-06-frame-anchors-full-body.jpg`
> （两张的人脸已做模糊处理）。

## 什么时候要读这一页

要「全身」「站姿」「三视图」「别裁脚」「别太近」这类要求时。不读这一页，最常见的结局是：
写了一大串 full body / entire body / both feet visible，出来的还是膝盖以上，脚被裁掉。

## 结论先说（这是实测出来的分寸，别夸大）

**带参考图时，镜头口令会失守；换画面位置锚点能救回来。**
**不带参考图时，两种写法都能出全身**（但口令仍然不是百分百保险）。

| 主体 | 有没有接参考图 | 写法 | 结果 | seed |
|---|---|---|---|---|
| 及膝蓝旗袍少女 | 有（人脸参考） | MJ 那串镜头口令 | **裁到膝盖以上，脚完全没进画面** | 20261161 |
| 同上 | 有 | 同一串镜头口令 | **裁到小腿** | 20261163 |
| 同上 | 有 | 同一串镜头口令 | **裁到小腿** | 20261164 |
| 同上 | 有 | 画面位置锚点 | 全身，鞋踩地、上下留白 | 20261162 |
| 中性长外套长裤 | 无 | 镜头口令 | 全身 | 20261171 |
| 中性长外套长裤 | 无 | 画面位置锚点 | 全身 | 20261172 |
| 中性灰长裙 | 无 | 镜头口令 | 全身（连脚趾都在） | 20261181 |
| 中性灰长裙 | 无 | 画面位置锚点 | 全身 | 20261182 |
| 中性炭灰旗袍 | 无 | 镜头口令 | 全身 | 20261191 |

要点：**同一个主体、同一串口令，连换两个 seed 都裁**；而同一主体换成位置锚点，一次到位。
但把参考图撤掉、只留文字，同一串口令又能出全身 —— 所以问题不在「Midjourney 的句式本身有毒」，
而在**参考图会把构图钉死**（这条脾性在本 skill 的「换机位」一节里也出现过：参考图接在 conditioning 上时，
构图由图片决定，文字很难掰回来）。

## 保底写法（有参考图时都用这个）

```
Composition anchors, measured on the frame: her shoes rest on the floor inside the
bottom tenth of the picture and the empty floor continues to the very bottom edge;
the top of her head sits inside the top fifth of the picture, leaving a clear gap of
backdrop above her hair; her whole silhouette from hairline to soles is inside the
frame with visible empty space at both the top and the bottom edges; she is small in
the frame, about three fifths of its height, seen from far away with a wide view.
```

中文同义版：

> 画面位置锚点，按画面量：她的鞋踩在画面底部十分之一以内的地面上，鞋下的空地一直延伸到画面最下沿；
> 头顶落在画面上部五分之一以内，头发上方留出一段干净背景；从发际线到鞋底整个人都在画面里，
> 画面顶部与底部都能看见空地；她在画面里偏小，约占画面高度的五分之三，远景、广角看过去。

## 失效写法（可作对照，不要单独依赖）

```
Full body character shot, camera positioned further back, an extreme long shot,
the entire body from head to toe fully visible inside the frame, both feet clearly
shown and not cropped, she occupies about sixty percent of the frame height, with
ample space above the head and below the feet, vertical composition.
```

这些是**镜头口令**（camera further back / extreme long shot / 60%），H3 对镜头参数与距离不敏感，
对「画面里能数的位置」敏感。

## 换算表：把「镜头话」改写成「画面话」

| 你要的效果 | 别写 | 写这个 |
|---|---|---|
| 别太近 | camera further back / wide shot | she occupies about three fifths of the frame height（要几成写几成） |
| 别裁脚 | both feet visible / no crop | her shoes rest on the floor inside the bottom tenth, empty floor below them to the very bottom edge |
| 头顶要留白 | ample space above the head | the top of her head sits inside the top fifth, clear backdrop above |
| 半身 | medium shot / waist-up | the frame cuts her at the waist，腰部以上在画面内，腰以下在画面外 |
| 特写 | close-up | her head fills about two thirds of the frame height（用占比，不用镜头名） |

> 前一行「别太近」、第二行「别裁脚」、第三行「头顶留白」是上表那组对照里直接验证过的。
> **「半身」与「特写」两行只是同一原理的延伸写法，本机没单独跑过对照**，用之前先出一张确认。

## 自检（出图后 3 秒判断）

1. 鞋底与画面下沿之间有没有一条空地？没有 → 脚被裁的风险已经在。
2. 头顶到画面上沿的距离，是不是大概画面的五分之一？明显更小 → 构图偏紧。
3. 人物高度占画幅几成？写的是六成、出来八成，说明「远一点」那半句没被吃进去。
4. 有没有接参考图？接了 → 直接上位置锚点，别只写口令。

## 三视图/角色表：脸被压到多少像素，眼睛就没了

画「一张横图里放三列」时，先算一笔账再动手。H3 单张出图有像素上限
(`MAX_PIXELS = 768×1344 = 1032192`)，所以：

| 版式 | 每列宽度 | 人物头高 | 眼睛约几像素 | 结果 |
|---|---|---|---|---|
| 1344×768 一张图塞三列 | 448 px | ≈110 px | ≈10 px | 放大 6 倍后眼睛是**两团暗红影子**，没有眼白/虹膜/瞳孔 |
| 每视角单图 768×1344，再 PIL 拼成 2304×1344 | 768 px | ≈200 px | ≈25 px | 放大 6 倍后眼白、虹膜、瞳孔、一个高光点都读得出来 |

对照：`examples/failure-10-eyes-lost-at-448px.jpg`（448 px 版的脸部放大 6 倍）、
`examples/success-10-eyes-readable-2304-sheet.jpg`（2304 拼版版的脸部放大 6 倍）。
两张都是 seed 20264001、同一套渲染锚、同一模型。

所以「三视图 / 角色设定表」的推荐做法不是「一张图里画三列」，而是：

1. 正面、侧面、背面**各出一张 768×1344**（背面必须用背面参考图，见 `multi-view-orientation.md`）；
2. 用 PIL 横向拼成 `768×3 × 1344`（这里是 2304×1344），白底补缝；
3. 需要交付小图时再整体降采样，别让它反过来决定每列的原始像素。

附带一条措辞教训（**属推断，未做隔离实验**）：第一版写的是照抄原画设定的 `narrow red eyes`，
出来就是两条细缝；第二版把部件写全（`a clean white sclera, a round crimson iris, a dark pupil, one crisp
white specular dot, a dark upper lash line above the iris, the fringe parts above the eyes`）才有眼睛。
因为措辞和分辨率是同时改的，**单独哪一个够不够，本机没验证过**；稳妥做法是两件一起做。

## 复现命令

本页所有对照都用同一张图跑的，那张图的唯一存档在 `h3-image-workflow` skill 里，不在这里重复第二份。
要复现，改三处即可：提示词段（换成上面对照里的写法）、`noise_seed`、`filename_prefix`；
带参考图与不带参考图的开关也在那份文件里写着。
