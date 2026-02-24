# PlantUML中文时序图使用指南

**文档版本**：1.0  
**更新时间**：2026年2月23日  
**项目名称**：社区化图书共享与推荐平台  
**适用版本**：系统实现设计（时序图）.md 全20个时序图

---

## 📖 目录

1. [快速开始](#快速开始)
2. [所有时序图列表](#所有时序图列表)
3. [代码特性说明](#代码特性说明)
4. [常见问题解答](#常见问题解答)
5. [使用最佳实践](#使用最佳实践)
6. [验证清单](#验证清单)

---

## 快速开始

### 方式1：在线编辑器（推荐）

最简单快速的方式，无需安装任何软件。

**步骤1：打开在线编辑器**
- 访问 [PlantUML 在线编辑器](https://www.plantuml.com/plantuml/uml/)

**步骤2：复制时序图代码**
- 打开 `系统实现设计（时序图）.md` 文件
- 找到需要的时序图代码块（从 `@startuml` 到 `@enduml`）
- 全选并复制整个代码块

**步骤3：粘贴并查看**
- 在在线编辑器左侧窗口粘贴代码
- 右侧会自动生成图形预览
- 所有中文文字应该能正确显示

**步骤4：导出**
- 点击右上角 "Download as" 按钮
- 选择PNG/SVG/PDF格式导出
- 保存到本地文件

### 方式2：VS Code插件

适合经常使用PlantUML的开发者。

**安装步骤**
1. 打开VS Code
2. 打开扩展市场（Ctrl+Shift+X）
3. 搜索 "PlantUML"
4. 安装官方插件或推荐的第三方插件
5. 安装完成后重启VS Code

**使用方式**
1. 打开 `系统实现设计（时序图）.md` 文件
2. 在任意时序图代码块前面按 Alt+D 预览
3. 点击"Save as"导出图片

### 方式3：本地部署

适合需要集成到CI/CD流程的专业团队。

**安装Java和PlantUML**
```bash
# 1. 安装 Java 11+ (已安装可跳过)
java -version

# 2. 下载 PlantUML jar 文件
# 访问 http://plantuml.com/download
# 下载 plantuml.jar

# 3. 验证安装
java -jar plantuml.jar -version
```

**生成图片**
```bash
# 方式A：从单个文件生成
java -jar plantuml.jar sequence_diagram.puml -o output_dir

# 方式B：递归处理整个目录
java -jar plantuml.jar "系统实现设计（时序图）.md" -o diagrams

# 方式C：生成PNG格式（默认）
java -jar plantuml.jar diagram.puml -tpng

# 方式D：生成SVG格式（可缩放）
java -jar plantuml.jar diagram.puml -tsvg

# 方式E：生成PDF格式（可打印）
java -jar plantuml.jar diagram.puml -tpdf
```

---

## 所有时序图列表

### 用户管理模块（4个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 1 | 用户登录 | `@startuml UserLoginSequence` | 用户登录认证流程，包含密码验证和Token生成 | 6 |
| 2 | 个人信息修改 | `@startuml UserProfileUpdateSequence` | 用户修改昵称、邮箱等个人信息 | 4 |
| 3 | 用户账号冻结 | `@startuml UserFreezeSequence` | 管理员冻结或解冻用户账号 | 4 |
| 4 | 用户账号删除 | `@startuml UserDeleteSequence` | 管理员删除用户及其所有关联数据 | 4 |

### 图书管理模块（5个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 5 | 图书添加 | `@startuml BookAddSequence` | 管理员添加新图书，包括文件上传 | 5 |
| 6 | 图书搜索 | `@startuml BookSearchSequence` | 用户按关键词搜索图书 | 4 |
| 7 | 图书更新 | `@startuml BookUpdateSequence` | 管理员修改图书信息 | 4 |
| 8 | 图书删除 | `@startuml BookDeleteSequence` | 管理员删除图书及其关联数据 | 4 |
| 9 | 图书收藏 | `@startuml BookCollectSequence` | 用户收藏或取消收藏图书 | 4 |

### 借阅管理模块（4个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 10 | 借阅创建 | `@startuml BorrowCreateSequence` | 用户借阅图书，包含库存和逾期检查 | 4 |
| 11 | 借阅查询 | `@startuml BorrowListSequence` | 用户查看自己的借阅记录 | 4 |
| 12 | 图书归还 | `@startuml BookReturnSequence` | 用户归还图书，包含逾期判断 | 4 |
| 13 | 借阅延期 | `@startuml BorrowDelaySequence` | 用户申请延期借阅 | 4 |

### 社交互动模块（3个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 14 | 书评发布 | `@startuml CommentPublishSequence` | 用户对已借图书发表评论 | 4 |
| 15 | 评论点赞 | `@startuml CommentLikeSequence` | 用户点赞或取消点赞评论 | 4 |
| 16 | 社区动态发布 | `@startuml PostPublishSequence` | 用户在社区发表动态 | 5 |

### 系统管理模块（3个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 17 | 分类管理 | `@startuml ClassificationManageSequence` | 管理员管理图书分类 | 4 |
| 18 | 标签管理 | `@startuml TagManageSequence` | 管理员管理图书标签 | 4 |
| 19 | 通知发布 | `@startuml NoticePublishSequence` | 管理员发布系统通知 | 5 |

### 推荐算法模块（1个）

| # | 时序图名称 | 代码标识 | 描述 | 参与者数 |
|----|----------|---------|------|---------|
| 20 | 推荐算法 | `@startuml RecommendAlgorithmSequence` | 协同过滤推荐算法实现流程 | 5 |

---

## 代码特性说明

### 1. 字体配置

所有时序图都已配置支持简体中文显示：

```plantuml
skinparam defaultFontName "Microsoft YaHei UI"
skinparam backgroundColor #FEFEFE
```

**说明**：
- `Microsoft YaHei UI` 是Windows系统内置的中文字体，支持完整的中文字符集
- `#FEFEFE` 背景颜色是浅白色，便于阅读
- 这些配置在所有20个时序图中都是一致的

### 2. 命名约定

**Actor（角色）中文命名**
- `用户` - 系统前端用户
- `管理员` - 系统后端管理员

**Participant（参与者）中文命名**
- `前端` - Vue.js前端应用
- `后端` - Django后端服务
- `数据库` - MySQL数据库
- `用户服务`、`图书服务` - 业务服务层

### 3. 消息格式

**API调用示例**
```
fe -> be: POST /myapp/index/user/login
note right: {username, password}
```
- HTTP方法和API路径保持不变
- 中文描述说明请求的内容

**数据库操作示例**
```
service -> db: SELECT * FROM b_user WHERE username=?
```
- 所有SQL语句保持原样不变
- 确保代码正确性

**条件分支示例**
```
alt 密码正确
    service --> be: {code: 0, msg: 登录成功, token}
else 密码错误
    service --> be: {code: 1, msg: 用户名或密码错误}
end
```
- alt/else条件改为中文
- 应答消息中文化

### 4. 代码结构

所有时序图都遵循统一的代码结构：

```
@startuml DiagramName
skinparam ... (配置)

actor 用户 as user
participant 前端 as fe
participant 后端 as be
... (其他参与者)

user -> fe: (消息流程开始)
... (完整业务流程)
deactivate fe

@enduml
```

---

## 常见问题解答

### Q1. 在PlantUML在线编辑器中显示乱码怎么办？

**解决方案**：
1. 检查文件是否保存为UTF-8编码
   - 在VS Code中，右下角选择"UTF-8"编码
2. 确保代码中包含字体配置：
   ```
   skinparam defaultFontName "Microsoft YaHei UI"
   ```
3. 在在线编辑器顶部菜单选择 Settings → Language 确保为 Chinese (Simplified)

### Q2. 如何在自己的文档中嵌入这些图表？

**Markdown嵌入方式**：
```markdown
![时序图](diagram.png)
```

**Word嵌入方式**：
- 导出为PNG图片
- 在Word中插入图片

**PowerPoint展示**：
- 导出为SVG格式（分辨率更高）
- 在幻灯片中插入

### Q3. 如何修改时序图中的内容？

**修改步骤**：
1. 在文本编辑器打开 `系统实现设计（时序图）.md`
2. 找到需要修改的时序图代码块
3. 修改演员、参与者或消息文本
4. 保存文件
5. 在在线编辑器粘贴新代码查看效果

**注意事项**：
- 不要修改API路径和SQL语句
- 不要修改函数调用和数据结构
- 仅修改显示文本部分

### Q4. 如何在CI/CD流程中自动生成这些图表？

**GitHub Actions示例**：
```yaml
name: Generate PlantUML Diagrams
on: [push]
jobs:
  plantuml:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: ggrossetie/plantuml-action@v1
        with:
          args: -v 系统实现设计（时序图）.md -o output
```

### Q5. 如何导出为PDF高质量版本？

**使用在线编辑器**：
1. 粘贴代码
2. 点击 "Download as" → "PDF"
3. 保存文件

**使用本地命令**：
```bash
java -jar plantuml.jar diagram.puml -tpdf -o output_dir
```

---

## 使用最佳实践

### 1. 文档保持一致性

**建议**：
- 将所有时序图统一放在同一文档中
- 按模块组织，便于查找
- 在文档中标注更新日期

**示例结构**：
```
# 系统实现设计文档

## 用户管理模块
### 4.1.1 用户登录流程
[时序图代码]

### 4.1.2 个人信息修改
[时序图代码]
```

### 2. 演示文稿使用

**建议**：
- 导出SVG格式保持清晰度
- 在幻灯片中调整图片大小
- 使用深色背景突出对比

### 3. 代码维护

**建议**：
- 更新业务流程时同时更新时序图
- 在代码注释中记录修改原因
- 定期检查API端点是否有变化

### 4. 版本控制

**建议**：
- 使用Git跟踪文档版本
- 在提交信息中说明修改内容
- 保留历史版本供参考

---

## 验证清单

使用此清单验证时序图的正确性：

### ✓ 语法检查
- [ ] 所有时序图都能在在线编辑器中正确显示
- [ ] 没有编译错误提示
- [ ] 所有中文文字都能正常显示

### ✓ 业务逻辑检查
- [ ] 所有actor和participant都正确标识
- [ ] 消息流程符合实际业务逻辑
- [ ] 条件分支（alt/else）覆盖所有情况

### ✓ API/数据库一致性检查
- [ ] 所有API端点正确（/myapp/index/*, /myapp/admin/*）
- [ ] 所有SQL语句正确（表名、字段名）
- [ ] 所有数据结构正确（请求/响应格式）

### ✓ 文档完整性检查
- [ ] 所有20个时序图都已包含
- [ ] 每个时序图都有清晰的描述
- [ ] 代码注释清楚易懂

### ✓ 交付检查
- [ ] 已导出高质量图片（PNG/SVG/PDF）
- [ ] 图片保存在指定目录
- [ ] 已备份原始代码文件

---

## 技术支持

### 常用资源
- [PlantUML官网](http://plantuml.com)
- [PlantUML用户指南](http://plantuml.com/zh/sequence-diagram)
- [PlantUML时序图文档](http://plantuml.com/zh/sequence-diagram)

### 获取帮助
- 查阅官方文档
- 在社区论坛提问
- 咨询项目技术主管

---

## 版本更新记录

| 版本 | 日期 | 修改内容 |
|------|------|--------|
| 1.0 | 2026-02-23 | 初始版本，支持20个中文时序图 |

---

**文档完成** ✓  
**最后更新**：2026年2月23日  
**作者**：系统设计团队
