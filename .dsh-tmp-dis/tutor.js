
(function () {
  var KEY = "ucf_tutor_v1";
  var STEPS = [
    { t: "欢迎：90 分钟学会改路点", hl: [],
      b: "<p>这不是说明书，是<strong>跟着做</strong>的练习。你只要照着点，每步都告诉你：<em>做什么 → 会看到什么 → 为什么</em>。</p>" +
         "<p>三件事：① 路点是什么 ② 编辑器怎么用 ③ 改完怎么进游戏。</p>" +
         "<p>练习场是<strong>空的</strong>，画坏了也不影响任何真地图。</p>" },
    { t: "第 1 步：打开练习场", hl: ["#sec-files", "#filelist"],
      b: "<p>看左边「打开」里，点 <span class='k'>练习场（空白）</span>。</p>" +
         "<p>打开后中间会出现一块空地，右边出现 3D 场景 —— 这就是你的沙盒。</p>" +
         "<p class='warn'>如果没有「打开」这一块，先刷新一下页面。</p>" },
    { t: "界面地图：三个区域", hl: ["#side", "#pane2", "#pane3"],
      b: "<p><strong>左栏</strong>= 设置和工具；<strong>中间</strong>= 2D 俯视图；<strong>右边</strong>= 3D 场景。</p>" +
         "<p>顶栏的 <span class='k'>节点 0</span> <span class='k'>边 0</span> 就是这张图现在有多少个点、多少条线，随时盯它。</p>" },
    { t: "2D 俯视图怎么动", hl: ["#pane2"],
      b: "<p>滚轮缩放；按住左键拖是平移；单击一个点会选中它（侧栏『点信息』显示坐标）。</p>" +
         "<p>你在这里看到的是<strong>地面平面图</strong>，箱子、台阶在这里只是一个点顶上的坐标。</p>" },
    { t: "3D 视图怎么动", hl: ["#pane3"],
      b: "<p>右键拖动转视角，滚轮拉近拉远。你应该能看到一块 40×40 的空地、3 个箱子、5 级台阶和一根柱子。</p>" +
         "<p>以后加点的时候，2D 里放位置、3D 里看它到底有没有悬空或者贴错面。</p>" },
    { t: "第 2 步：切到『加点』", hl: ["#b-mode-add"],
      b: "<p>左栏「编辑」里点 <span class='k'>加点</span>（快捷键 <span class='k'>A</span>）。</p>" +
         "<p>这个模式下在 2D 视图点一下 = 在那个位置放一个路点。</p>" },
    { t: "第 3 步：放第一个点", hl: ["#pane2", "#c-nodes"],
      b: "<p>在中间的空地上<strong>单击一下</strong>。会立刻出现一个点，顶栏「节点」从 0 变 1。</p>" +
         "<p>为什么重要：路点就是<strong>『人能站的位置』</strong>，机器人的寻路全靠它。</p>" },
    { t: "第 4 步：围一个 10×10 的方框", hl: ["#pane2"],
      b: "<p>再点 3 下，四个点大致摆成一个正方形（顶栏节点 = 4）。</p>" +
         "<p>不用很准，后面可以拖。先体会『一个点 = 一个坐标』。</p>" },
    { t: "第 5 步：连线", hl: ["#b-mode-link"],
      b: "<p>点 <span class='k'>连线</span>（快捷键 <span class='k'>E</span>），然后<strong>先后点两个点</strong>，就连出一条边。</p>" +
         "<p>连 4 条，围成环路。顶栏「边」= 4。</p>" +
         "<p>为什么重要：<strong>边 = 两点之间能直着走过去</strong>。有边机器人才会走。边太长（超过 2.1 m）游戏不认，这是 A* 的 maxDistance。</p>" },
    { t: "第 6 步：检查孤立点", hl: ["#b-iso", "#c-iso"],
      b: "<p>点 <span class='k'>孤立点</span>（<span class='k'>G</span>）：它会跳到「没有任何边的点」，这类点只会标红、实际没用。</p>" +
         "<p>全部连上的话它就报『没有孤立点』。这个按钮以后是你的自检工具。</p>" },
    { t: "第 7 步：故意改坏，再修好", hl: ["#b-del", "#b-undo", "#b-redo"],
      b: "<p>选中一个点 → 点 <span class='k'>删点</span>（<span class='k'>Delete</span>）：点没了，连在它身上的边一起断。</p>" +
         "<p>再点 <span class='k'>撤销</span>（<span class='k'>Ctrl+Z</span>）就回来；<span class='k'>重做</span>是 <span class='k'>Ctrl+Y</span>。</p>" +
         "<p>放心乱来：练习场没有真数据。</p>" },
    { t: "第 8 步：保存，看它写了什么", hl: ["#b-save", "#s-txt", "#s-target"],
      b: "<p>点 <span class='k'>保存并应用</span>（<span class='k'>Ctrl+S</span>）。它写的是<strong>改动清单</strong>，不是整张图：几行 <span class='k'>node add</span> / <span class='k'>edge add</span>。</p>" +
         "<p>清单文件按<strong>指纹</strong>命名：指纹 = 这张图所有点坐标的校验和，用来保证『编辑套到了对的那张图』。</p>" +
         "<p>练习场指纹是 <span class='k'>n0-0000000000000000</span>，所以写出来的文件在游戏里只会落到『本来就 0 个点』的图上。</p>" +
         "<p class='warn'>第 6 课会进游戏验证：看《学习_路点入门.md》第 6 节。</p>" }
  ];
  var i = 0, open = false, lastHl = [];
  var el = document.getElementById("tutor"), body = document.getElementById("tut-body");
  var pg = document.getElementById("tut-pg"), bar = document.getElementById("tut-bar");

  function clearHl() {
    lastHl.forEach(function (e) { e.classList.remove("tut-hl"); });
    lastHl = [];
  }
  function draw() {
    clearHl();
    var s = STEPS[i];
    body.innerHTML = "<h4>" + s.t + "</h4>" + s.b;
    pg.textContent = (i + 1) + "/" + STEPS.length;
    bar.style.width = ((i + 1) / STEPS.length * 100).toFixed(1) + "%";
    document.getElementById("tut-prev").disabled = (i === 0);
    document.getElementById("tut-next").textContent = (i === STEPS.length - 1) ? "完成" : "下一步";
    (s.hl || []).forEach(function (sel) {
      Array.prototype.forEach.call(document.querySelectorAll(sel), function (e) {
        e.classList.add("tut-hl"); lastHl.push(e);
      });
    });
    try { localStorage.setItem(KEY, JSON.stringify({ step: i })); } catch (e) {}
  }
  function show(on) {
    open = on;
    el.classList.toggle("on", on);
    if (on) draw(); else clearHl();
  }
  document.getElementById("tut-next").onclick = function () {
    if (i >= STEPS.length - 1) { show(false); return; }
    i++; draw();
  };
  document.getElementById("tut-prev").onclick = function () { if (i > 0) { i--; draw(); } };
  document.getElementById("tut-close").onclick = function () { show(false); };

  var tb = document.getElementById("topbar"), grow = tb && tb.querySelector(".grow");
  if (tb && grow) {
    var btn = document.createElement("button");
    btn.className = "btn mini"; btn.id = "b-tutor"; btn.textContent = "新手引导";
    btn.title = "打开 / 继续新手引导（练习场）";
    btn.onclick = function () { show(!open); };
    tb.insertBefore(btn, grow);
  }
  var saved = null;
  try { saved = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { saved = null; }
  if (saved && typeof saved.step === "number") { i = Math.max(0, Math.min(STEPS.length - 1, saved.step)); show(true); }
  else {
    setTimeout(function () { show(true); }, 1200);   /* 第一次打开自动弹出来 */
  }
})();
