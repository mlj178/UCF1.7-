
import re, io
p = r"D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\ucf_mod\\tools\\navview.html"
s = io.open(p, encoding="utf-8").read()
blocks = re.findall(r"<script>(.*?)</script>", s, re.S)
print("script blocks:", len(blocks), "last len:", len(blocks[-1]))
io.open(r"D:\trae_project\ucf1.7-modifier\.dsh-tmp-dis\tutor.js", "w", encoding="utf-8").write(blocks[-1])
print("has unclosed template?", s.count("<script>"), s.count("</script>"))
