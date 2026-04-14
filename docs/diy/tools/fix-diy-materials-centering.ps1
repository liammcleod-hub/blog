$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'

$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}

if (-not $shopDomain -or -not $token) {
  throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile"
}

$headersGet = @{ 'X-Shopify-Access-Token' = $token }
$headersPut = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }

$themeId = '196991385938' # Maerz 2026 (main theme)
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)

$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value

# Center variable number of items:
# - Use auto-fit so "2 items" becomes "2 columns" (not leftmost 2 of 4)
# - Cap max width to 4 columns so it never becomes 5 columns on ultra-wide screens.

$fixed = $orig

$needleDesktop = 'grid-template-columns: repeat(4, minmax(0, 220px));\n      justify-content: center;\n      gap: 20px;'
$replaceDesktop = 'grid-template-columns: repeat(auto-fit, minmax(220px, 220px));\n      justify-content: center;\n      gap: 20px;\n      max-width: calc(4 * 220px + 3 * 20px);\n      margin-left: auto;\n      margin-right: auto;'

# Same but with escaped newlines (the asset JSON uses \\n inside the custom_liquid string).
$needleDesktopEsc = 'grid-template-columns: repeat(4, minmax(0, 220px));\\n      justify-content: center;\\n      gap: 20px;'
$replaceDesktopEsc = 'grid-template-columns: repeat(auto-fit, minmax(220px, 220px));\\n      justify-content: center;\\n      gap: 20px;\\n      max-width: calc(4 * 220px + 3 * 20px);\\n      margin-left: auto;\\n      margin-right: auto;'

$fixed = $fixed.Replace($needleDesktop, $replaceDesktop).Replace($needleDesktopEsc, $replaceDesktopEsc)

$needleTablet = 'grid-template-columns: repeat(2, minmax(0, 220px));'
$replaceTablet = 'grid-template-columns: repeat(auto-fit, minmax(220px, 220px));\n        max-width: calc(2 * 220px + 1 * 20px);\n        margin-left: auto;\n        margin-right: auto;'

$needleTabletEsc = 'grid-template-columns: repeat(2, minmax(0, 220px));'
$replaceTabletEsc = 'grid-template-columns: repeat(auto-fit, minmax(220px, 220px));\\n        max-width: calc(2 * 220px + 1 * 20px);\\n        margin-left: auto;\\n        margin-right: auto;'

$fixed = $fixed.Replace($needleTablet, $replaceTablet).Replace($needleTabletEsc, $replaceTabletEsc)

# Validate JSON before pushing.
$jsonOk = $true
try { $null = $fixed | ConvertFrom-Json -ErrorAction Stop } catch { $jsonOk = $false }
if (-not $jsonOk) { throw "Refusing to push: $assetKey is not valid JSON after update." }

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 50
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

# Quick live verification: ensure the new max-width rule appears in the served HTML at least once.
$repl = [string][char]0xFFFD
$urls = @(
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj',
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)
$checks = @()
foreach ($u in $urls) {
  $cacheBust = $u + '?v=' + [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
  $resp = Invoke-WebRequest -Uri $cacheBust -UseBasicParsing
  $ms = New-Object System.IO.MemoryStream
  $resp.RawContentStream.CopyTo($ms)
  $html = [Text.Encoding]::UTF8.GetString($ms.ToArray())
  $checks += [pscustomobject]@{
    url = $u
    status = [int]$resp.StatusCode
    has_replacement_char = $html.Contains($repl)
    has_materials_max_width = $html.Contains('max-width: calc(4 * 220px + 3 * 20px)')
  }
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  changed = $changed
  checks = $checks
} | ConvertTo-Json -Compress

