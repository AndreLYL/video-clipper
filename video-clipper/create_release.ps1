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
$titleLine = Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -First 1
$title = $titleLine -replace '^#\s*', ''

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
# 注意：使用--title参数明确指定标题，避免从文件读取时出现编码问题
# 将标题转换为UTF-8字节数组再转回字符串，确保编码正确
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($title)
$titleUtf8 = [System.Text.Encoding]::UTF8.GetString($utf8Bytes)

Write-Host "`n正在创建Release..." -ForegroundColor Yellow
gh release create $Version `
    --title $titleUtf8 `
    --notes-file $ReleaseNotesFile `
    $ExeFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nRelease创建成功！" -ForegroundColor Green
    Write-Host "链接: https://github.com/AndreLYL/video-clipper/releases/tag/$Version" -ForegroundColor Cyan
} else {
    Write-Host "`nRelease创建失败！" -ForegroundColor Red
    exit 1
}

