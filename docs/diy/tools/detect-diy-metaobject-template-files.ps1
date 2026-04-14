$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$headers = @{ 'X-Shopify-Access-Token' = $token }
$themeId = '196991385938' # Maerz 2026

function TryFetch([string]$key) {
  $encodedKey = [System.Uri]::EscapeDataString($key)
  $url = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
  try {
    $r = Invoke-RestMethod -Uri $url -Headers $headers -Method Get
    return [pscustomobject]@{ key = $key; exists = $true; bytes = ($r.asset.value.Length) }
  } catch {
    return [pscustomobject]@{ key = $key; exists = $false; error = $_.Exception.Message }
  }
}

$keys = @(
  'templates/metaobject/diy_experience.json',
  'templates/metaobject/diy_experience.standard.json',
  'templates/metaobject/diy_experience.default.json'
)

$results = foreach ($k in $keys) { TryFetch $k }
[pscustomobject]@{ theme_id = $themeId; results = $results } | ConvertTo-Json -Compress

