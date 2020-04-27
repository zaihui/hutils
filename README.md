# HUtils, a charming python web util-library.

[![Build](https://github.com/zaihui/hutils/workflows/Build/badge.svg)](https://github.com/zaihui/hutils)
[![Package](https://img.shields.io/pypi/v/hutils.svg)](https://pypi.python.org/pypi/hutils)
[![Versions](https://img.shields.io/pypi/pyversions/hutils.svg)](https://pypi.python.org/pypi/hutils)

本项目为我司 [@zaihui](https://github.com/zaihui) 在后端开发中，
积攒的比较好用的各类基类函数。
除了基础的类型变换，
还有 django/~~grpc~~ 相关的一系列功能。

让我们简单看一段用上了 hutils 以后的效果：

```python
import hutils

# 使用前
def create_user(data):
    try:
        uid, age, phone, created_at = data["uid"], data["age"], data["phone"], data["created_at"]
        # 此处做一系列类型验证，或者用个 marshmallow 之类的库来验证 :)
        return User(uid=uid, age=age, phone=phone, created_at=created_at)
    except Exception as ex:
        logger.exception(ex)

# 使用后
@hutils.mutes(log=True)
def create_user(data):
    uid, age, phone, created_at = hutils.get_data(data, "uid", "age", "phone", "created_at")
    created_at = created_at or hutils.yesterday()
    if not all([hutils.is_uuid(uid), hutils.is_int(age), hutils.is_phone(phone)]):
        return None
    return User(uid=uid, age=age, phone=phone, created_at=created_at)
```

详细的文档可以参见下方。
总而言之，`hutils` 库的目标就是：

**Let coding in python be a pleasure!**


## Installation

```shell script
pip install hutils
```


## Document

```python
# 在本节文档用法中，
# 我们会从具体的使用场景来介绍 hutils 里的基类函数库。
# 详尽的参数可以读源码，
# 我们尽最大努力保持着源码的可读性。

# 使用了尽可能短的包名，
# 就是为了直接 `import hutils` 的，
# 切记不要 `from hutils import *`
import hutils

# 有时你想把一些 bytes/str 的变量统一转成 str
x = b'bytes' or 'string'
print(hutils.bytes_to_str(x))

# 在计算金额时，你需要做两位小数的算数
# 而在返给前段时，又要去掉最末的 0
interest = hutils.quantize(98.0 * 0.05)
print(f'利息为¥{hutils.normalize(interest)}元')

# 你可能需要给前端返回两个字典的合集，
# 并转换成 json
print(hutils.format_json(hutils.merge_dicts(
    {'a': 1, 'b': 2},
    {'a': 1, 'c': []},
)))

# 有时从前端的数据中，你要取值
request_data = {'key1': 'value', 'key2': 'value2', 'key3': 'value3'}
print(hutils.get_data(request, 'key1', 'key2', 'key3'))

# 前端会传性别进来，
# 对应后端要有常量的验证
class Genders(hutils.TupleEnum):
    MALE = 0, '男性'
    FEMALE = 1, '女性'
    UNKNOWN = 2, '未知'
print(Genders.chinese_choices())
with hutils.catches(raises=HTTP400Error):
    gender = Genders(request_data['gender'])

# 以及各种无副作用的短函数
start, end = hutils.yesterday(), hutils.tomorrow()
start_morning, end_evening = hutils.datetime_combine(start, end)
print(f'有效期起始日为昨日凌晨({hutils.datetime_to_str(start_morning)})')
```

关于更多的文档，
请直接在源码里查看吧 :)


## Contribution

假如你想增加新的基类函数，
请先[提交一个 issue 说明一下](https://github.com/zaihui/hutils/issues/new)。

本项目的代码需要符合以下标准：

- **必须:** 单元测试必须要通过
  - 依赖第三方库时(比如 `django`), 不能因为缺少依赖而导致整个 `import hutils` 都挂了。
- **必须:** 基础语法风格检查必须要通过
- **推荐:** 每个函数都要有对应的单元测试


## License

[MIT License](/LICENSE)


## Others

欢迎各位大佬提 PR/Issue 把你们觉得 好用的/写得不够完善的/缺少单元测试 的功能也提交进来~

最后献上一首 `The Zen of Python`:

```
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```
