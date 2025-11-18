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

# 设置控制台输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 读取发布说明（确保UTF-8编码）
$notes = Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -Raw

# 从发布说明的第一行提取标题（去掉#号）
$title = (Get-Content -Path $ReleaseNotesFile -Encoding UTF8 -First 1) -replace '^#\s*', ''

Write-Host "创建Release: $Version" -ForegroundColor Green
Write-Host "标题: $title" -ForegroundColor Cyan
Write-Host "EXE文件: $ExeFile" -ForegroundColor Cyan

# 使用GitHub CLI创建Release
# 注意：使用--title参数明确指定标题，避免从文件读取时出现编码问题
gh release create $Version `
    --title $title `
    --notes-file $ReleaseNotesFile `
    $ExeFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nRelease创建成功！" -ForegroundColor Green
    Write-Host "链接: https://github.com/AndreLYL/video-clipper/releases/tag/$Version" -ForegroundColor Cyan
} else {
    Write-Host "`nRelease创建失败！" -ForegroundColor Red
    exit 1
}

