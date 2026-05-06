# 视频生成平台适配指南

## 即梦AI

### 角色描述最佳实践
- 角色描述放在 prompt 前 1/3 位置
- 使用自然中文，不要翻译成英文（即梦中文理解优于英文）
- 同角色多次生成使用固定 seed 可减少漂移
- 面部锚点每句话用逗号分隔，不换行（节省 token 窗口）

### 多角色 prompt 结构
```
[场景环境描述]
角色1：{姓名}，{面部锚点精简}，{服饰}，{动作}
角色2：{姓名}，{面部锚点精简}，{服饰}，{动作}
[镜头参数] [光线] [风格]
```

### 已知限制
- 侧面角度下眼睛特征衰减严重，需额外强调眉形和鼻梁
- 远景角色的面部会大幅简化，需靠服饰和身高区分

---

## 可灵AI

### 角色描述最佳实践  
- 面部特征使用英文描述更稳定
- 场景和动作用中文
- 整体 prompt 以英文为主时角色一致性更好
- 推荐使用 negative prompt 排除不需要的特征

### prompt 结构（中英混合）
```
[Environment description in English]
{Character Name}: {face anchors in English}, {body in English},
wearing {costume in English} {specific item in Chinese if unique}.
[Action description in Chinese or English]
[Camera parameters in English] [Lighting in English]
```

### 英文面部锚点速查表
- 鹅蛋脸 → oval face
- 杏仁眼 → almond eyes  
- 双眼皮 → double eyelid
- 柳叶眉 → gently arched eyebrows
- 鼻梁挺直 → straight nose bridge
- 暖白皮 → fair warm-toned skin
- 哑光 → matte complexion

### 已知限制
- 中文服饰描述（如"汉服"）中文效果优于英文
- 动态镜头中角色面部漂移比即梦更大

---

## 跨平台策略

1. **角色锚点用 YAML 存一份，两种格式各导出一份**
2. **先在即梦跑定妆照（静态面部），通过后再进可灵跑动态**
3. **同一角色在同一平台的 seed 固定（记录在角色 YAML 里）**
4. **可灵的 negative prompt 从角色的禁用色和禁用材质直接生成**
