from importlib import import_module


async def get_novels_info(class_name, novels_name):
    novels_module = import_module(
        "Easy.fetcher.{}.{}_novels".format('novels_factory', class_name))
    # 获取对应渠道实例化对象
    novels_info = await novels_module.start(novels_name)
    return novels_info