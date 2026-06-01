from probo.context import ProboContextProvider


__Context = ProboContextProvider()

def __context_settings(context:ProboContextProvider,**settings):
    for k,v in settings.items():
        key = context.get(k)
        if not key:
            context.put(k,v)
    return settings

def get_global_context()->ProboContextProvider:
    __context_settings(__Context,
    cart_item_count=0,
    )
    return __Context
