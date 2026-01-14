# Set encoding to UTF8 to handle potential symbols
$OutputEncoding = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 1. PATH CONFIGURATION
$OBS_PATH = "D:\Documents\Obsidian Vault\lizechat\lize-chat-astro\src\content\blog"
$WEB_PATH = "D:\lize-chat\lize-chat-astro\src\content\blog"
$WEB_ROOT = "D:\lize-chat\lize-chat-astro"

Write-Host ">>> START: Moving files from Obsidian..." -ForegroundColor Cyan

# 2. FILE MOVING LOGIC
if (Test-Path $OBS_PATH) {
    Copy-Item -Path "$OBS_PATH\*" -Destination $WEB_PATH -Recurse -Force
    Write-Host ">>> SUCCESS: Files copied to web folder." -ForegroundColor Green
} else {
    Write-Host ">>> ERROR: Path not found: $OBS_PATH" -ForegroundColor Red
    Start-Sleep -Seconds 10
    return
}

# 3. GIT DEPLOYMENT
Set-Location -Path $WEB_ROOT
Write-Host ">>> Pushing to GitHub..." -ForegroundColor Cyan

git add --all 
$status = git status --porcelain
if ($status) {
    git commit -m "auto-sync: obsidian-update $(Get-Date -Format 'MM-dd HH:mm')"
    git push
    Write-Host ">>> DONE: Site is updating on Vercel!" -ForegroundColor Green
} else {
    Write-Host ">>> INFO: No changes found." -ForegroundColor Yellow
}

Write-Host "Window closing in 5 seconds..."
Start-Sleep -Seconds 5