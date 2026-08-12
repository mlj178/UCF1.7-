def handle_event(context, event, payload):
    if event != "result":
        return
    ok = payload.get("ok", False)
    if ok:
        bots = payload.get("bots", 0)
        fail = payload.get("fail", 0)
        context.log(f"✅ 聚怪结果: 传送成功{bots} 失败{fail}")
    else:
        context.log(f"❌ 聚怪失败: {payload.get('msg', '未知')}")
