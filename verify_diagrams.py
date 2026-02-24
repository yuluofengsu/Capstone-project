#!/usr/bin/env python3
# -*- coding: utf-8 -*-

\"\"\"
PlantUML 时序图验证脚本
用于检查所有20个时序图代码的完整性和中文兼容性

使用方法：
    python3 verify_diagrams.py

输出：
    - 每个时序图的验证结果
    - 总体统计信息
    - 错误日志（如有）
\"\"\"

import re
import sys
from pathlib import Path

# 定义所有应该存在的时序图
EXPECTED_DIAGRAMS = [
    'UserLoginSequence',
    'UserProfileUpdateSequence',
    'UserFreezeSequence',
    'UserDeleteSequence',
    'BookAddSequence',
    'BookSearchSequence',
    'BookUpdateSequence',
    'BookDeleteSequence',
    'BookCollectSequence',
    'BorrowCreateSequence',
    'BorrowListSequence',
    'BookReturnSequence',
    'BorrowDelaySequence',
    'CommentPublishSequence',
    'CommentLikeSequence',
    'PostPublishSequence',
    'ClassificationManageSequence',
    'TagManageSequence',
    'NoticePublishSequence',
    'RecommendAlgorithmSequence'
]

class DiagramValidator:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.content = self.file_path.read_text(encoding='utf-8')
        self.errors = []
        self.warnings = []
        self.results = {}
        
    def validate(self):
        \"\"\"执行完整验证\"\"\"
        print('=' * 70)
        print('PlantUML 中文时序图验证报告')
        print('=' * 70)
        print()
        
        # 检查文件编码
        self._check_encoding()
        
        # 检查每个时序图
        for diagram_name in EXPECTED_DIAGRAMS:
            self._check_diagram(diagram_name)
        
        # 打印总体结果
        self._print_summary()
        
    def _check_encoding(self):
        \"\"\"检查文件编码\"\"\"
        try:
            self.content.encode('utf-8')
            print('✓ 文件编码：UTF-8 OK')
        except UnicodeEncodeError:
            self.errors.append('文件编码不是UTF-8')
            print('✗ 文件编码：非UTF-8格式')
        print()
        
    def _check_diagram(self, diagram_name):
        \"\"\"检查单个时序图\"\"\"
        print(f'检查时序图：{diagram_name}')
        
        # 检查是否存在
        start_pattern = f'@startuml {diagram_name}'
        end_pattern = '@enduml'
        
        if start_pattern not in self.content:
            self.results[diagram_name] = False
            self.errors.append(f'{diagram_name}: 不存在')
            print(f'  ✗ 时序图不存在')
            print()
            return
        
        # 提取时序图代码块
        start_idx = self.content.find(start_pattern)
        end_idx = self.content.find(end_pattern, start_idx)
        
        if end_idx == -1:
            self.results[diagram_name] = False
            self.errors.append(f'{diagram_name}: @enduml 标记不完整')
            print(f'  ✗ 缺少 @enduml 标记')
            print()
            return
        
        diagram_code = self.content[start_idx:end_idx+len(end_pattern)]
        
        # 检查中文字体配置
        if 'skinparam defaultFontName' in diagram_code or 'skinparam fontName' in diagram_code:
            print(f'  ✓ 包含字体配置')
        else:
            self.warnings.append(f'{diagram_name}: 缺少字体配置')
            print(f'  ⚠ 警告：缺少字体配置')
        
        # 检查是否包含中文
        if self._has_chinese(diagram_code):
            print(f'  ✓ 包含中文内容')
        else:
            print(f'  ⚠ 警告：可能缺少中文内容')
        
        # 检查是否有英文actor/participant
        if self._has_english_display(diagram_code):
            print(f'  ⚠ 警告：仍包含英文显示文本')
        else:
            print(f'  ✓ 已完全中文化')
        
        # 检查API端点完整性
        api_patterns = [
            r'/myapp/(?:index|admin)/\\w+',
        ]
        api_found = any(re.search(pattern, diagram_code) for pattern in api_patterns)
        if api_found or 'SELECT' in diagram_code or 'UPDATE' in diagram_code:
            print(f'  ✓ 保留了API/SQL逻辑')
        
        # 检查是否有语法错误
        if self._check_syntax(diagram_code):
            print(f'  ✓ 语法检查通过')
            self.results[diagram_name] = True
        else:
            print(f'  ✗ 可能存在语法错误')
            self.results[diagram_name] = False
        
        print()
    
    def _has_chinese(self, text):
        \"\"\"检查文本是否包含中文\"\"\"
        return bool(re.search(r'[\\u4e00-\\u9fff]', text))
    
    def _has_english_display(self, text):
        \"\"\"检查是否有英文显示文本（排除代码部分）\"\"\"
        # 排除通常应该是英文的部分
        exclude_keywords = [
            'SELECT', 'UPDATE', 'INSERT', 'DELETE', 'FROM', 'WHERE',
            'POST', 'GET', 'PUT', 'PATCH', 'DELETE',
            'token', 'username', 'password', 'email', 'mobile',
            'code', 'msg', 'data',
            'verify_credentials', 'validate_', 'get_', 'check_',
            'user_id', 'book_id', 'classification_id',
            'APIResponse', 'b_user', 'b_book', 'b_borrow',
        ]
        
        # 查找可能的英文消息
        messages = re.findall(r': [^\\n]*', text)
        for msg in messages:
            msg_clean = msg.replace(':', '').strip()
            # 如果是短消息且全是英文，就是需要中文化的
            if msg_clean and len(msg_clean) < 30:
                is_code = any(keyword in msg_clean for keyword in exclude_keywords)
                if not is_code and msg_clean[0].isupper():
                    # 可能是英文消息
                    if not self._has_chinese(msg_clean):
                        return True
        
        return False
    
    def _check_syntax(self, code):
        \"\"\"基本语法检查\"\"\"
        checks = [
            ('@startuml' in code, '缺少@startuml'),
            ('@enduml' in code, '缺少@enduml'),
            (code.count('actor') > 0 or code.count('participant') > 0, '缺少actor或participant'),
            (code.count('->') > 0 or code.count('-->') > 0, '缺少消息流'),
        ]
        
        for check, error_msg in checks:
            if not check:
                self.errors.append(f'语法错误: {error_msg}')
                return False
        
        # 检查成对的 activate/deactivate
        activates = code.count('activate')
        deactivates = code.count('deactivate')
        if activates != deactivates:
            self.warnings.append(f'activate/deactivate 不配对 ({activates} vs {deactivates})')
        
        return True
    
    def _print_summary(self):
        \"\"\"打印总结统计\"\"\"
        print('=' * 70)
        print('验证总结')
        print('=' * 70)
        print()
        
        total = len(EXPECTED_DIAGRAMS)
        passed = sum(1 for v in self.results.values() if v)
        failed = total - passed
        
        print(f'总时序图数：{total}')
        print(f'通过验证：{passed} ✓')
        print(f'未通过验证：{failed} ✗')
        print()
        
        if self.errors:
            print('错误信息：')
            for error in self.errors:
                print(f'  ✗ {error}')
            print()
        
        if self.warnings:
            print('警告信息：')
            for warning in self.warnings:
                print(f'  ⚠ {warning}')
            print()
        
        if not self.errors and not self.warnings:
            print('✓ 所有验证通过，无错误和警告！')
            print()
        
        # 详细结果表
        print('详细检查结果：')
        print('-' * 70)
        for i, diagram_name in enumerate(EXPECTED_DIAGRAMS, 1):
            status = '✓' if self.results.get(diagram_name, False) else '✗'
            print(f'{i:2d}. {status} {diagram_name}')
        
        print()
        print('=' * 70)

def main():
    \"\"\"主函数\"\"\"
    # 查找 系统实现设计（时序图）.md 文件
    script_dir = Path(__file__).parent
    md_file = script_dir / '系统实现设计（时序图）.md'
    
    if not md_file.exists():
        # 尝试其他可能的位置
        possible_paths = [
            Path.cwd() / '系统实现设计（时序图）.md',
            script_dir.parent / '系统实现设计（时序图）.md',
        ]
        
        for path in possible_paths:
            if path.exists():
                md_file = path
                break
        else:
            print('错误：无法找到 系统实现设计（时序图）.md 文件')
            print(f'请在文件所在目录运行此脚本，或指定文件路径')
            sys.exit(1)
    
    print(f'验证文件：{md_file}')
    print()
    
    validator = DiagramValidator(md_file)
    validator.validate()
    
    # 返回退出码
    if validator.errors:
        sys.exit(1)
    elif validator.warnings:
        sys.exit(0)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
