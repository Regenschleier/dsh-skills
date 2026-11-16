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

## 自检（出图后 3 秒判断）

1. 鞋底与画面下沿之间有没有一条空地？没有 → 脚被裁的风险已经在。
2. 头顶到画面上沿的距离，是不是大概画面的五分之一？明显更小 → 构图偏紧。
3. 人物高度占画幅几成？写的是六成、出来八成，说明「远一点」那半句没被吃进去。
4. 有没有接参考图？接了 → 直接上位置锚点，别只写口令。

## 复现命令

见 `../references/api-graph.md` 里的 JSON 骨架，改动三处即可复现本页对照：
`6.inputs.prompt`（换成上面对照写法）、`8.inputs.noise_seed`、`14.inputs.filename_prefix`；
要「带参考图」就把 `5` 号 LoadImage 接到 `6.inputs["images.image_0"]`，不要接 `vae`。
