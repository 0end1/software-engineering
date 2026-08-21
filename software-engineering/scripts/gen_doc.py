#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_doc.py — 软件工程规范文档生成器

为已有（或新建）项目生成标准的软件工程文档：需求规格说明书、设计说明书、
测试计划、测试报告、可行性研究报告。文档内容基于软件工程技能的模板，
自动套用项目名称并写入目标项目目录。

用法:
    python3 gen_doc.py --name <项目名> [--type <文档类型>] [--out <目录>] [--model <模式>]

参数:
    --name   项目名称（必填），套用到文档标题
    --type   文档类型（默认 all）: srs | design | test-plan | test-report |
                       feasibility | all
    --out    输出目录 (默认 ./docs)
    --model  开发模式（写入设计/测试文档，默认 agile）

示例:
    python3 gen_doc.py --name mstores --type srs --out ./docs
    python3 gen_doc.py --name mstores --model waterfall
"""

import argparse
import os
import sys

DOC_TYPES = ["srs", "design", "test-plan", "test-report", "feasibility", "all"]


def gen_srs(name, model=None):
    return f"""# 软件需求规格说明书（SRS）— {name}

> 模板来源：software-engineering 技能 assets/srs-template.md

## 1. 引言
### 1.1 目的
<描述本文档目的>

### 1.2 范围
<系统名称、解决问题、目标用户、边界>

### 1.3 术语
| 术语 | 定义 |
|------|------|
| <术语> | <定义> |

## 2. 总体描述
### 2.1 产品视角
<系统在业务中的位置>

### 2.2 用户特征
| 角色 | 描述 | 场景 |
|------|------|------|
| <角色> | <描述> | <场景> |

### 2.3 运行环境
- OS / 运行时 / 硬件 / 网络

## 3. 具体需求
### 3.1 功能需求
| 编号 | 描述 | 优先级 | 来源 |
|------|------|-------|------|
| REQ-F-001 | <功能> | 高 | <用户> |

### 3.2 非功能需求
- 性能 / 安全 / 可靠性 / 可用性 / 可维护性

### 3.3 接口需求
- 用户 / 硬件 / 软件 / 通信接口

## 4. 需求追踪矩阵
| 编号 | 优先级 | 对应设计 | 测试用例 |
|------|-------|---------|---------|
| REQ-F-001 | 高 | | |
"""


def gen_design(name, model):
    return f"""# 设计说明书（概要/详细）— {name}

> 模式：{model}。模板来源：software-engineering 技能 assets/design-doc-template.md

## 1. 引言
目的 / 范围 / 术语 / 参考资料(SRS)

## 2. 总体设计
### 2.1 系统架构
<架构图 + 说明>

### 2.2 模块划分
| 模块 | 职责 | 依赖 |
|------|------|------|
| <模块> | <职责> | <依赖> |

### 2.3 技术选型
| 层面 | 选型 | 理由 |
|------|------|------|
| 语言/框架 | | |
| 数据库 | | |

### 2.4 数据库设计
<ER 图 + 表结构>

## 3. 接口设计
<模块间/外部接口>

## 4. 详细设计（模块）
### 4.1 模块 <X>
- 类/结构、关键算法、异常与边界处理

## 5. 安全与性能
<认证、缓存、索引、限流、事务>
"""


def gen_test_plan(name, model):
    return f"""# 测试计划 — {name}

> 模式：{model}。参考：software-engineering 技能 references/testing-maintenance.md

## 1. 测试目标与范围
<覆盖功能/非功能需求>

## 2. 测试层次
- [ ] 单元测试
- [ ] 集成测试
- [ ] 系统测试
- [ ] 验收测试

## 3. 测试类型
- 黑盒：等价类划分、边界值分析
- 白盒：分支/路径覆盖
- 灰盒：集成与 API

## 4. 环境与进度
<环境、资源、排期>

## 5. 缺陷与验收
- 严重程度：致命/严重/一般/轻微
- 验收标准：<何时可发布>
"""


def gen_test_report(name, model=None):
    return f"""# 测试报告 — {name}

> 参考：software-engineering 技能 references/testing-maintenance.md

## 1. 测试概述
- 时间 / 人员 / 范围

## 2. 执行情况
| 层次 | 用例数 | 执行数 | 通过 | 通过率 |
|------|-------|-------|------|-------|
| 单元 | | | | |
| 集成 | | | | |
| 系统 | | | | |

## 3. 缺陷统计
| 严重程度 | 数量 | 已修复 | 遗留 |
|---------|------|-------|------|
| 致命 | | | |
| 严重 | | | |
| 一般 | | | |
| 轻微 | | | |

## 4. 遗留风险与发布建议
<质量评估与是否发布>
"""


def gen_feasibility(name, model=None):
    return f"""# 可行性研究报告 — {name}

> 参考：software-engineering 技能 references/software-lifecycle.md

## 1. 项目概述
- 背景 / 目标 / 范围

## 2. 现有系统分析
<现状与不足>

## 3. 可行性维度
- 技术可行性
- 经济可行性（成本/收益/ROI）
- 操作可行性
- 法律可行性
- 进度可行性

## 4. 风险分析
<主要风险与对策>

## 5. 结论与建议
<是否立项、推荐方案>
"""


GENERATORS = {
    "srs": ("SRS.md", gen_srs),
    "design": ("design.md", gen_design),
    "test-plan": ("test-plan.md", gen_test_plan),
    "test-report": ("test-report.md", gen_test_report),
    "feasibility": ("feasibility.md", gen_feasibility),
}


def main():
    parser = argparse.ArgumentParser(description="软件工程规范文档生成器")
    parser.add_argument("--name", required=True, help="项目名称")
    parser.add_argument("--type", default="all", choices=DOC_TYPES,
                        help="文档类型 (默认 all)")
    parser.add_argument("--out", default="./docs", help="输出目录 (默认 ./docs)")
    parser.add_argument("--model", default="agile",
                        help="开发模式，写入 design/test-plan (默认 agile)")
    args = parser.parse_args()

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    types = list(GENERATORS.keys()) if args.type == "all" else [args.type]
    for t in types:
        fname, fn = GENERATORS[t]
        content = fn(args.name, args.model)
        full = os.path.join(out_dir, fname)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已生成文档: {full}")

    print(f"\n共生成 {len(types)} 份文档到 {out_dir}")


if __name__ == "__main__":
    main()
