$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$themeId = '196991385938' # Maerz 2026
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
$headersGet = @{ 'X-Shopify-Access-Token' = $token }

$value = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value

$markers = @(
  '/cart/add.js',
  'Menge',
  'Ausw',
  'Ausgew',
  'diy-',
  'materials',
  'variant',
  '<style'
)

$found = @()
foreach ($m in $markers) {
  $ixm = $value.IndexOf($m)
  if ($ixm -ge 0) {
    $start = [Math]::Max(0, $ixm - 180)
    $len = [Math]::Min(1000, $value.Length - $start)
    $found += [pscustomobject]@{ marker = $m; index = $ixm; snippet = $value.Substring($start, $len) }
  }
}

$first = $null
if ($found.Count -gt 0) { $first = $found | Sort-Object index | Select-Object -First 1 }

$materials = $found | Where-Object { $_.marker -eq 'materials' } | Select-Object -First 1
$materialsSnippet = $materials.snippet

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  has_any_marker = ($found.Count -gt 0)
  first_marker = $first.marker
  first_index = $first.index
  first_snippet = $first.snippet
  materials_index = $materials.index
  materials_snippet = $materialsSnippet
  all_markers_found = ($found | Select-Object marker,index)
} | ConvertTo-Json -Compress
