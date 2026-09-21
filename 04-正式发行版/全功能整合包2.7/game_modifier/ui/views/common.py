def bind_view_handles(target, handles):
    items = handles.items() if isinstance(handles, dict) else vars(handles).items()
    for name, value in items:
        setattr(target, name, value)
