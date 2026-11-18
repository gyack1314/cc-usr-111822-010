# 柔性工位扩张计划

项目按来源版本保存业务资料，已有 orders、cells、support 环节。现有订单、工位和技术员单期计划未考虑共享支援、任务切换及返工对扩张承诺的共同影响。

运行与检查：

    python -m unittest discover -s tests -v
    python -m compileall -q flexible_factory tests
    python -m flexible_factory.cli data/example.json
