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
$themeId = '196991385938' # Maerz 2026

function GetAsset([string]$key) {
  $encodedKey = [System.Uri]::EscapeDataString($key)
  $url = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
  (Invoke-RestMethod -Uri $url -Headers $headersGet -Method Get).asset.value
}

$needle = 'grid-template-columns: repeat(4, minmax(0, 220px));'
$assetKeys = @(
  'templates/metaobject/diy_experience.json',
  'config/settings_data.json'
)

$hits = @()
foreach ($k in $assetKeys) {
  $v = GetAsset $k
  $ix = $v.IndexOf($needle)
  $hits += [pscustomobject]@{
    key = $k
    has_needle = ($ix -ge 0)
    index = $ix
  }
}

[pscustomobject]@{
  theme_id = $themeId
  needle = $needle
  hits = $hits
} | ConvertTo-Json -Compress

