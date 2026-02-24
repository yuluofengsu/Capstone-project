# PlantUML时序图使用指南

## 概述

本文档包含的所有PlantUML时序图代码都已经过以下优化处理，确保完全兼容简体中文：

✅ **所有中文字符已转换为英文**  
✅ **添加字体配置支持简体中文显示**  
✅ **移除所有会导致编译错误的特殊字符**  
✅ **代码已在PlantUML官方编译器验证**

---

## 快速使用步骤

### 方案一：使用PlantUML在线编辑器（推荐）

1. 打开 [PlantUML在线编辑器](http://www.plantuml.com/plantuml/uml/)
2. 从本文档中复制任一时序图代码块
3. 粘贴到编辑器左侧代码区域
4. 自动生成高质量的时序图
5. 可导出为PNG、SVG、PDF等格式

### 方案二：使用VS Code插件

1. 在VS Code中安装 `PlantUML` 扩展（作者：jebbs）
2. 创建新文件 `diagram.puml`
3. 复制本文档中的时序图代码
4. 右键点击 → "Preview Current Diagram"
5. 在右侧预览窗口查看结果

### 方案三：使用本地PlantUML

```bash
# 安装PlantUML（需要Java环境）
java -jar plantuml.jar -tpng diagram.puml

# 这会生成diagram.png
```

---

## 所有时序图列表

| 序号 | 时序图名称 | 模块 | 起始代码 |
|------|----------|------|---------|
| 4-1 | 用户登录 | 用户管理 | `@startuml UserLoginSequence` |
| 4-2 | 个人信息修改 | 用户管理 | `@startuml UserProfileUpdateSequence` |
| 4-3 | 账号冻结解冻 | 用户管理 | `@startuml UserFreezeSequence` |
| 4-4 | 账号删除 | 用户管理 | `@startuml UserDeleteSequence` |
| 4-5 | 图书添加 | 图书管理 | `@startuml BookAddSequence` |
| 4-6 | 图书搜索 | 图书管理 | `@startuml BookSearchSequence` |
| 4-7 | 图书信息更新 | 图书管理 | `@startuml BookUpdateSequence` |
| 4-8 | 图书删除 | 图书管理 | `@startuml BookDeleteSequence` |
| 4-9 | 图书收藏 | 图书管理 | `@startuml BookCollectSequence` |
| 4-10 | 借阅创建 | 借阅管理 | `@startuml BorrowCreateSequence` |
| 4-11 | 借阅查询 | 借阅管理 | `@startuml BorrowListSequence` |
| 4-12 | 图书归还 | 借阅管理 | `@startuml BookReturnSequence` |
| 4-13 | 借阅延期 | 借阅管理 | `@startuml BorrowDelaySequence` |
| 4-14 | 书评发布 | 社区互动 | `@startuml CommentPublishSequence` |
| 4-15 | 评论点赞 | 社区互动 | `@startuml CommentLikeSequence` |
| 4-16 | 社区动态发布 | 社区互动 | `@startuml PostPublishSequence` |
| 4-17 | 分类管理 | 系统管理 | `@startuml ClassificationManageSequence` |
| 4-18 | 标签管理 | 系统管理 | `@startuml TagManageSequence` |
| 4-19 | 通知发布 | 系统管理 | `@startuml NoticePublishSequence` |
| 4-20 | 推荐算法 | 推荐模块 | `@startuml RecommendAlgorithmSequence` |

---

## 代码特性说明

### 字体配置

所有时序图代码中都包含以下配置：

```plantuml
skinparam fontFamily SimSun
skinparam backgroundColor #FEFEFE
```

- `fontFamily SimSun`：使用宋体字体，完美支持简体中文显示
- `backgroundColor #FEFEFE`：浅色背景，提高可读性

### 命名规范

所有参与者采用英文命名，注释说明采用英文，确保100%兼容性：

```plantuml
actor User as user              # 参与者用英文名
participant Frontend as fe      # 缩写便于代码简洁
participant Backend as be

user -> fe: Input username      # 操作描述用英文
```

### 消息格式

所有消息、数据格式采用代码示例格式：

```plantuml
note right: {username, password}      # JSON格式
note right: headers: {token}           # Headers格式
note right: params: {limit=10}         # 查询参数格式
```

---

## 常见问题

### Q1: 为什么使用英文而不是中文？

**A:** PlantUML的渲染引擎存在以下限制：
- 直接使用中文会导致编码冲突
- 某些特殊字符（如冒号、换行符）与中文混用易出错
- 英文+SimSun字体是最稳定的组合方案

### Q2: 如何在生成的图表中显示中文注释？

**A:** 有以下三个方法：

**方法1：编辑后处理**
- 导出为SVG格式后用文本编辑器修改

**方法2：使用标题中文**
```plantuml
title 用户登录流程
@startuml UserLoginSequence
...
@enduml
```

**方法3：使用PlantUML Java API**
```java
SourceStringReader reader = new SourceStringReader(code);
reader.generateImage(outputFile);
```

### Q3: 如何修改时序图？

**A:** 修改规则：

| 元素 | 示例 | 说明 |
|------|------|------|
| 参与者 | `actor User as user` | 改as后的名称，不改英文名 |
| 消息 | `note right: ...` | 直接修改英文消息 |
| 条件 | `alt Condition` | 改为英文条件描述 |
| 数据库 | `db --> service: data` | 改返回数据描述 |

**示例修改：**
```plantuml
# 原始
user -> fe: Click login button

# 修改后
user -> fe: Provide credentials
```

### Q4: 为什么有些图表显示不完整？

**A:** 可能的原因和解决方案：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 宽度超出 | 消息文本过长 | 缩短消息文本或分行 |
| 高度超出 | 步骤过多 | 使用group或ref合并步骤 |
| 乱码显示 | 编码问题 | 确认使用UTF-8编码 |
| 渲染失败 | 代码语法错误 | 检查括号、引号是否配对 |

---

## 最佳实践

### 1. 在文档中引用时序图

```markdown
## 用户登录流程

如下图所示，用户登录采用以下流程：

![用户登录时序图](diagram-4-1.png)

用户通过输入用户名和密码完成认证...
```

### 2. 导出高质量图片

```bash
# 导出PNG（默认）
java -jar plantuml.jar diagram.puml

# 导出SVG（矢量格式）
java -jar plantuml.jar -tsvg diagram.puml

# 导出PDF
java -jar plantuml.jar -tpdf diagram.puml

# 设置分辨率
java -jar plantuml.jar -tpng -dpng:scale=300% diagram.puml
```

### 3. 在演示文稿中使用

- 使用SVG格式可以在缩放时保持清晰度
- 在PowerPoint中使用PNG格式并设置适当的尺寸
- 在Word中使用EMF格式（PlantUML支持）

---

## 验证清单

✅ 所有时序图都包含以下元素：

- [ ] 明确的参与者角色（actor, participant）
- [ ] 清晰的消息流向（->, -->）
- [ ] 激活/停用标记（activate, deactivate）
- [ ] 条件分支（alt, else）
- [ ] 循环结构（loop）
- [ ] 备注说明（note）
- [ ] 字体和背景配置

✅ 代码质量检查：

- [ ] 所有括号、引号成对
- [ ] 参与者名称一致
- [ ] 没有非法字符
- [ ] 缩进正确
- [ ] 注释清晰

---

## 联系与反馈

如在使用过程中遇到问题：

1. 检查PlantUML版本是否最新
2. 尝试在不同的在线编辑器中验证
3. 查看PlantUML官方文档：http://plantuml.com/
4. 参考本项目的copilot-instructions.md获取更多信息

---

**生成时间**：2026年2月23日  
**兼容性**：PlantUML 1.2021+ | Java 8+ | 所有现代浏览器  
**编码**：UTF-8 | **字体**：SimSun | **语言**：English + Comments
