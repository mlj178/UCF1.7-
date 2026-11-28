<#
.SYNOPSIS
    把 unity-navmesh 从 dev 最新提交里彻底去掉并强推，让 GitHub 上的 303 个 LFS 对象变成"无人引用"。

.DESCRIPTION
    背景：06-测试/ucf_mod/unity-navmesh/ 里有 303 个文件是 git-lfs 指针
    （Unity PackageCache 里的小图片，本地 LFS 缓存 10.3 MB）。
    普通 git rm + commit 只会让它们从 tip 消失，历史里还引用着 —— GitHub 不会回收。
    必须把那一笔提交改写掉，再强推。

    这个脚本只改一笔提交（HEAD），只动这一条路径，其它内容原样保留。
    改写后：git lfs ls-files 应为空；GitHub 上的对象变成无人引用，等它 GC。

.PARAMETER DryRun
    只做检查并打印计划，不动任何东西。

.PARAMETER LocalOnly
    只在本地改写提交，不推送（网络不通时用）。

.EXAMPLE
    .\purge-lfs-unity.ps1 -DryRun
    .\purge-lfs-unity.ps1
#>
param(
    [switch]$DryRun,
    [switch]$LocalOnly,
    [switch]$PushOnly,
    [string]$Remote = 'github',
    [string]$Branch = 'dev'
)

$ErrorActionPreference = 'Stop'

# 用 git 的仓库根当工作目录。
# 注意：不能用 .ucfroot 往上找 —— 那个标记在 06-测试\ucf_mod（比仓库根浅一层），
# cwd 落在子目录里时 pathspec '06-测试/ucf_mod/unity-navmesh' 一根都对不上（2026-11-28 踩过）。
$root = (& git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if (-not $root) { throw "拿不到 git 仓库根（$PSScriptRoot 不在仓库里？）" }
$target = '06-测试/ucf_mod/unity-navmesh'
Write-Host "仓库根: $root"

Push-Location $root
try {
    # ---------- 只推送（本地已经 -LocalOnly 改写过了）----------
    if ($PushOnly) {
        Write-Host "HEAD  : $((git rev-parse --short HEAD).Trim())"
        Write-Host "推送  : $Remote/$Branch"
        git push --force-with-lease $Remote $Branch
        if ($LASTEXITCODE -ne 0) { throw "推送失败（exit $LASTEXITCODE）：网络或凭据问题，修好后重跑 -PushOnly" }
        Write-Host "完成。GitHub 上的 LFS 对象已无人引用，等它 GC。"
        return
    }

    # ---------- 前置检查 ----------
    $cur = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($cur -ne $Branch) { throw "当前分支是 $cur，不是 $Branch。先 git switch $Branch" }

    $head = (git rev-parse HEAD).Trim()
    $remoteRef = "$Remote/$Branch"
    $rhead = (git rev-parse $remoteRef 2>$null)
    if ($rhead) { $rhead = $rhead.Trim() }
    if ($rhead -and $rhead -ne $head) {
        throw "本地 HEAD($($head.Substring(0,7))) 和 $remoteRef($($rhead.Substring(0,7))) 不一致：先 git pull，别硬改"
    }

    $commits = @(git log --format=%H --all -- $target)
    if ($commits.Count -eq 0) { Write-Host "unity-navmesh 已经不在任何提交里，无需处理"; return }
    if ($commits.Count -ne 1) { throw "这条路径出现在 $($commits.Count) 个提交里，不能只改 HEAD。停手，人工处理" }
    if ($commits[0].Trim() -ne $head) {
        throw "unity-navmesh 在提交 $($commits[0].Substring(0,7))，不是 HEAD $($head.Substring(0,7))。这个脚本只会改 HEAD，停手"
    }

    $staged = @(git diff --cached --name-only)
    if ($staged.Count -gt 0) { throw "索引里还有 $($staged.Count) 个暂存改动：先 git restore --staged 清空，避免被 amend 一起提进去" }

    $inIndex = @(git ls-files -- $target).Count
    if ($inIndex -eq 0) { throw "pathspec '$target' 在索引里一个文件都没有：路径不对或已被删掉，确认后再说" }
    Write-Host "检查通过："
    Write-Host "  当前分支      : $cur"
    Write-Host "  HEAD          : $($head.Substring(0,7))"
    Write-Host "  $remoteRef : $($rhead.Substring(0,7))"
    Write-Host "  涉及提交      : 1 个（就是 HEAD）"
    Write-Host "  索引里的文件  : $inIndex 个"
    Write-Host "  LFS 指针文件  : $((git lfs ls-files | Measure-Object).Count) 个"

    if ($DryRun) {
        Write-Host ""
        Write-Host "DryRun：接下来会执行"
        Write-Host "  git rm -r --cached -- $target"
        Write-Host "  git commit --amend --no-edit"
        Write-Host "  git push --force-with-lease $Remote $Branch"
        Write-Host "没有做任何改动。"
        return
    }

    # ---------- 改写 HEAD ----------
    git rm -r --cached --quiet -- $target
    git commit --amend --no-edit --quiet
    $new = (git rev-parse HEAD).Trim()
    Write-Host "已改写：$($head.Substring(0,7)) -> $($new.Substring(0,7))"

    $left = (git lfs ls-files | Measure-Object).Count
    Write-Host "改写后 LFS 指针文件：$left 个（应为 0）"

    if ($LocalOnly) {
        Write-Host "只改了本地，没推。网络恢复后跑： git push --force-with-lease $Remote $Branch"
        return
    }

    # ---------- 强推 ----------
    Write-Host "强推到 $Remote/$Branch ..."
    git push --force-with-lease $Remote $Branch
    if ($LASTEXITCODE -ne 0) { throw "推送失败（exit $LASTEXITCODE）。本地已改写，网络/PAT 修好后重跑 git push --force-with-lease $Remote $Branch" }
    Write-Host "完成。GitHub 上的 LFS 对象已无人引用，等它 GC。"
}
finally {
    Pop-Location
}
