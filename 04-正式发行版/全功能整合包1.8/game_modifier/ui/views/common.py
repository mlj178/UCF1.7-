def bind_view_handles(target, handles):
    for name, value in vars(handles).items():
        setattr(target, name, value)
