# character-design 案例图

这里只放**一对能说明问题的对照图**，每张都标了「怎么来的、结果为什么算成/算败」。
两张的人脸都做了模糊处理：这两张是从用户的私人参考照片跑出来的，只保留构图证据，不公开可识别的人像。

## failure-05-body-lock-words-cropped.jpg

- 想做什么：一张从头到脚的全身站姿（及膝旗袍少女，接了一张人脸参考图）。
- 提示词怎么写的：只写了镜头口令——`full body character shot, camera positioned further back, extreme long shot, entire body from head to toe fully visible, both feet clearly shown, she occupies about sixty percent of the frame height, ample space above the head and below the feet, vertical composition`。
- 结果：画到小腿就停，脚完全没有进画面。
- 复现情况：同一主体、同一串口令，换 seed 20261163 / 20261164 各跑一次，**两次都还是裁**。
- 病因：接参考图时，构图会被参考图钉住；H3 对「镜头多远、什么景别」这类口令不敏感。
- 改法：见 `references/framing-lock.md` 的「保底写法」。

## success-06-frame-anchors-full-body.jpg

- 同一套人物、同一张参考图、同一个渲染锚，只把构图段换成了**画面位置锚点**：`her shoes rest on the floor inside the bottom tenth … the empty floor continues to the very bottom edge; the top of her head sits inside the top fifth …; she is small in the frame, about three fifths of its height, seen from far away with a wide view`。
- 结果：头到脚全在画面内，两只鞋踩在地上、鞋下还有一条空地板，头顶留白，一次过。

## 一条重要的补测（别把上一节的结论扩大化）

把参考图整根撤掉、只用文字描述同一个及膝旗袍（seed 20261191），那串镜头口令**又能出全身**；
换成中性长外套长裤（20261171/20261172）与中性长裙（20261181/20261182）也一样，两种写法都出全身。
所以正确的说法是：**镜头口令不是永远失效，而是带参考图时容易被构图钉死；位置锚点是保底写法。**

两张都是本机 MiniMax H3 实跑：int8 fl2va、768×1344、30 步、`images.image_0` 保留、`vae` 那根断开。

## success-07-three-view-turnaround.jpg

- 想做什么：一张横排三列的角色资产图（左：面颈锁骨特写；中：严格正面全身；右：严格背面全身）。
- 怎么做的：1344×768（32 的倍数，等于 MAX_PIXELS 上限）、30 步、conditioning 节点**不接参考图也不接 vae**，版式全部用画面位置锚点写死（`three equal columns … left third … middle third … right third`）。
- 结果：三列一次到位，同一角色、同一地板线、无边框无标签；seed 20261301。同参数的另外两次（20261302 / 20261311）也都是三列结构，说明版式稳定，差异在脸与细节。
- 已知偏差：特写列容易被画得过大、挤掉脖子与锁骨；`armoured bodice` 会被读成光滑曲面壳而不是甲片。
