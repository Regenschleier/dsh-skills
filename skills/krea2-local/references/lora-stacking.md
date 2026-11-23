# Krea2 LoRA 叠加：实测档位与失效边界

验证环境：ComfyUI 本地后端，`krea2_turbo_int8_convrot` + `qwen3vl_4b_fp8_scaled`(krea2) + `qwen_image_vae`，8 步 / cfg 1.0 / euler / simple / denoise 1.0，832×1248，seed 20261400–20261504。日期 2026-11-23。

## 一、五个 LoRA 各是什么（实测，不是卖家描述）

| 文件 | 真实作用 | 建议权重 | 副作用 |
|---|---|---|---|
| `krea2_style_reference.safetensors` | 风格参考/画质基准，几乎恒开 | 0.9 | 权重过低会让画面回到「默认动漫感」 |
| `krea2_auroraNostalgia_v1.1`（极光旧梦） | 电影感定向光 + 金边轮廓 + 雪雾光斑 + 胶片调 | **1.0**（1.4 起自作加耳饰/帽标） | 强光下会改脸型 |
| `Detailer_Beauty_Krea2`（Detailer - Krea2 project） | **美颜**：皮肤更平、腮红更显、唇更饱满、整体偏暖 | 0.7–1.3 | 不增加织物/金属纹理，别指望它「加细节」 |
| `si_wooupp_style_v1` | 服饰与配件的层次（皮带、扣具、毛领、补丁） | 0.4–1.0 | 高权重会加设定外装备 |
| `NIJISIS_krea2_V2` | 更「精修动漫/网图美女」的方向 | 0.8 | 压低逆光雪雾，和极光旧梦抢方向 |

> 三个没能拿到：`light_krea2_loraholic`（同名版只在 SeaArt，公开镜像里只有 `brightness_krea2_loraholic`）、`NIJISIS_krea2_V_2` 的 TensorArt 原版、其余 SeaArt 独占模型。

## 二、三档配方与结果

### 轻档 `0.9 / 1.0 / 0.7 / 0.4`

- 用途：全身、远景、需要保住角色设定的时候。
- 结果：接近「干净的半写实 CG」，光有但不抢戏；**能按构图锚点拍出全身**（`sc5d` 是这一档跑出来的，靴底仍有轻微裁切）。

### 过载档 `0.9 / 1.6 / 1.3 / 1.0`

- 用途：近景、半身、封面。
- 结果：逆光金边、金属扣、毛领、皮革补丁、层次项链全出，画面质感明显上一档。
- 代价：**会自动补设定外的细节**（耳饰、帽徽、胸口纹样）、脸型变尖、发色变浅；六景里连试三次全身都失败，全部收成近景/半身。

### 单层档 `0.9 / 1.0 / 0 / 0`

- 用途：大场景、多人、要明显看到环境的时候。
- 结果：只加调色与轮廓光，角色完全不变，构图最听话。

## 三、叠加规则的来源

叠加不是线性相加，而是每层都在改写同一批权重：

1. **总强度预算 2.0–2.3**：四个权重加起来超过这个数，出图开始出现「不属于这个角色的东西」。
2. **顺序：先风格后细节**。把 Detailer 放在主风格之前，美颜会被后面的风格层覆盖掉。
3. **滑块类只留一个**：brightness/light 这种滑块本质在调同一组通道，两个一起用会互相抵消甚至反转。
4. **每加一层，加载时间变长，采样速度基本不变**（8 步固定）。
5. **新 LoRA 先单独跑 `off` 对照**：同 seed、只改这一层权重 0 → 看清它到底动什么。

## 四、构图与强度的冲突（重要）

同一句构图锚点（`her whole figure from beanie to boots fits inside the frame, head near the top fifth, boots touching the bottom fifth`）：

| 档位 | 结果 |
|---|---|
| 轻档 | 全身成立（靴底略裁） |
| 过载档 | 连续三次都收成半身或大腿以上；加 `low angle`、加 `no close-up / cropped boots` 都没用 |

结论：**风格强度会压过构图锚点**。要全身就别开重档；要重档就别指望全身。这条已同步写进 `skills/character-design/references/framing-lock.md`。

## 五、复现命令

```powershell
# 单层对照（只换这一行 strength）
"9":  { "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["1",0], "lora_name": "krea2_style_reference.safetensors", "strength_model": 0.9 } }
"11": { "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["9",0], "lora_name": "krea2_auroraNostalgia_v1.1.safetensors", "strength_model": 1.6 } }
"12": { "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["11",0],"lora_name": "Detailer_Beauty_Krea2.safetensors", "strength_model": 1.3 } }
"13": { "class_type": "LoraLoaderModelOnly", "inputs": { "model": ["12",0],"lora_name": "si_wooupp_style_v1.safetensors", "strength_model": 1.0 } }
```

对照图：`Desktop\ai图\极光旧梦对比\三档对比.png`（off / 1.0 / 1.4）、`四LoRA叠加_1.0+0.7+0.4.png`、`基准_过载档_1.6+1.3+1.0.png`。
