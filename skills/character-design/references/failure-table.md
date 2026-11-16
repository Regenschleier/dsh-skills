# 失败对照表（症状 → 病因 → 改哪一段）

> 用法：出图不满意时，先在下表第一列找到最像的症状，按第三列只改那一段，不要通篇重写。

| 症状 | 病因 | 改哪里 |
|---|---|---|
| 出来是个十来岁的小孩 | 只写了「精致、柔、大眼睛」，没有年龄与骨相 | 第 1 段加一句 `a woman of about twenty-two, an adult rather than a child, slim neck, defined jaw, chin to a soft point` |
| 整张塌成平涂动漫、没有材质 | 写了 `mature / delicate / narrow-lidded` 这类「成熟脸」词 | 删掉这些词，把渲染锚放回第一句，加 `semi-realistic materials, subsurface skin` |
| 变成真人照片，用户说「这是人类」 | 出现 `pores / photographic grain / skin texture`，或参考图接了 vae | 删毛孔与颗粒词；参考图节点的 vae 断开（VAEDecode 那根照接） |
| 用户说「诡异」「像鬼」 | 瓷面 + 大眼 + 空走廊 + 通篇死灰，四样凑齐 | 按 SKILL.md 第五节四条逐条改：皮肤加活气、眼神给动作、光给温度、显式禁止 `blank stare / porcelain mask` |
| 换了机位，出来的还是原构图 | `images` 还接着参考图；或动作段留着上一张的 `stomp / kick` | 删 `images.image_0` 这个带点的键；动作段整段重写 |
| 十二张里八张长得一样 | 每张都写了同一套机位句式（35mm、人物偏左、看画外） | 每张把焦距、机位高度、人物朝向、构图三分法写成不同值 |
| 人物的脸被参考图拖走（发色、下巴都变了） | 参考图权重过大（接了 vae） | 断 vae；或把参考图换成「自己已经出好的一张 CG 图」裁一刀再用（CG 进 CG 出） |
| 暗调压不下来，画面发亮 | 只写了 `dark`，没有可判定的顶光上限 | 加 `printed two stops under` 与 `the brightest tone no brighter than pale smoke` |
| 想要横向光刃，出来是散光 | 6 步蒸馏把光晕细节啃掉了 | 改 30 步 int8；或写成 `a single unbroken streak across the lower third` |
| 手指多一根、出现第二个人 | 没写禁止项 | 第 8 段补 `no extra fingers, no second character` |
| 画面很漂亮但没有生命感 | 光均匀、没有热源、没有具体动作 | 给一个动作（正在合上杯盖）+ 一个热源（咖啡的蒸汽），光改成环境冷、人暖 |
| 服装细节全糊在一起 | 提示词里写了五件以上的单品 | 只留镜头里看得见的 2–3 件，其余删掉 |
