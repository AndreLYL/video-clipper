# 创建GitHub Release脚本
# 确保正确处理UTF-8编码，避免乱码问题

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [Parameter(Mandatory=$true)]
    [string]$ReleaseNotesFile,
    
    [Parameter(Mandatory=$true)]
    [string]$ExeFile
)

# 设置UTF-8编码（关键步骤，避免乱码）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

# 读取发布说明（确保UTF-8编码）
$notes = Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -Raw

# 从发布说明的第一行提取标题（去掉#号）
# 如果标题包含中文，建议使用英文标题避免编码问题
$titleLine = Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -First 1
$titleFromFile = $titleLine -replace '^#\s*', ''

# 检查标题是否包含中文字符
if ($titleFromFile -match '[\u4e00-\u9fff]') {
    Write-Host "警告: 标题包含中文字符，可能在某些环境下出现乱码" -ForegroundColor Yellow
    Write-Host "建议: 使用英文标题，例如 'VideoClipper $Version'" -ForegroundColor Yellow
    Write-Host "当前标题: $titleFromFile" -ForegroundColor Cyan
    $useEnglishTitle = Read-Host "是否使用英文标题? (Y/N, 默认N)"
    if ($useEnglishTitle -eq 'Y' -or $useEnglishTitle -eq 'y') {
        $title = "VideoClipper $Version"
        Write-Host "使用英文标题: $title" -ForegroundColor Green
    } else {
        $title = $titleFromFile
    }
} else {
    $title = $titleFromFile
}

Write-Host "创建Release: $Version" -ForegroundColor Green
Write-Host "标题: $title" -ForegroundColor Cyan
Write-Host "EXE文件: $ExeFile" -ForegroundColor Cyan

# 验证文件是否存在
if (-not (Test-Path $ExeFile)) {
    Write-Host "错误: EXE文件不存在: $ExeFile" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $ReleaseNotesFile)) {
    Write-Host "错误: 发布说明文件不存在: $ReleaseNotesFile" -ForegroundColor Red
    exit 1
}

# 使用GitHub CLI创建Release
# 关键：使用--notes参数直接传递内容，而不是--notes-file，避免文件编码问题
# 同时设置代码页为UTF-8 (65001)
Write-Host "`n正在创建Release..." -ForegroundColor Yellow

# 设置代码页为UTF-8
chcp 65001 | Out-Null

# 读取发布说明内容（UTF-8编码）
$notesContent = Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -Raw

# 使用--notes参数直接传递内容，而不是--notes-file
# 这样可以确保编码正确传递
gh release create $Version `
    --title $title `
    --notes $notesContent `
    $ExeFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nRelease创建成功！" -ForegroundColor Green
    Write-Host "链接: https://github.com/AndreLYL/video-clipper/releases/tag/$Version" -ForegroundColor Cyan
} else {
    Write-Host "`nRelease创建失败！" -ForegroundColor Red
    exit 1
}

