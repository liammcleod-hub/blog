$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$headersGet = @{ 'X-Shopify-Access-Token' = $token }
$themeId = '196991385938'
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey
$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value

$template = $orig | ConvertFrom-Json -ErrorAction Stop

$rows = @()
foreach ($k in $template.sections.PSObject.Properties.Name) {
  $sec = $template.sections.$k
  $blockKeys = @()
  if ($null -ne $sec.blocks) {
    if ($sec.blocks -is [System.Collections.IDictionary]) {
      $blockKeys = @($sec.blocks.Keys)
    } else {
      $blockKeys = @($sec.blocks.PSObject.Properties.Name)
    }
  }
  $rows += [pscustomobject]@{
    section = $k
    type = $sec.type
    has_custom_liquid_materials_grid = ($blockKeys -contains 'custom_liquid_materials_grid')
    has_custom_liquid_steps_grid = ($blockKeys -contains 'custom_liquid_steps_grid')
    block_count = $blockKeys.Count
    first_blocks = ($blockKeys | Select-Object -First 12)
  }
}

$rows | ConvertTo-Json -Compress -Depth 6

