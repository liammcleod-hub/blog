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
$headersPut = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }

$themeId = '196991385938' # Maerz 2026 (main theme)
$assetKey = 'templates/metaobject/diy_experience.json'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value
$template = $orig | ConvertFrom-Json -ErrorAction Stop

# 1) Add a stable scroll anchor into the steps custom-liquid block.
$stepsLiquid = $template.sections.section_PQQgbR.blocks.group_KJ6ae3.blocks.group_TaPk8k.blocks.group_tUmKXk.blocks.custom_liquid_steps_grid.settings.custom_liquid
if (-not $stepsLiquid) { throw "Could not find steps custom liquid at expected path." }

if (-not ($stepsLiquid -match 'id=\"diy-steps-anchor\"')) {
  # Insert anchor immediately after the opening wrapper div.
  $openNeedle = '<div id="diy-steps-{{ block.id }}" class="diy-steps">'
  $ix = $stepsLiquid.IndexOf($openNeedle)
  if ($ix -ge 0) {
    $insert = $openNeedle + "`n  <div id=""diy-steps-anchor""></div>`n"
    $stepsLiquid = $stepsLiquid.Substring(0, $ix) + $insert + $stepsLiquid.Substring($ix + $openNeedle.Length)
  } else {
    throw "Could not find steps wrapper opening tag to insert anchor."
  }
  $template.sections.section_PQQgbR.blocks.group_KJ6ae3.blocks.group_TaPk8k.blocks.group_tUmKXk.blocks.custom_liquid_steps_grid.settings.custom_liquid = $stepsLiquid
}

# 2) Replace the hero button block with a custom-liquid block that:
# - links to download_file when present
# - otherwise scrolls to #diy-steps-anchor
$heroButton = $template.sections.section_Hca4zN.blocks.group_rjq9Lc.blocks.button_wEwTDT
if (-not $heroButton) { throw "Could not find hero button block button_wEwTDT." }

$buttonLiquid = @'
{% assign diy = closest.metaobject.diy_experience %}
{% assign file = diy.download_file.value %}
{% assign label = diy.download_button_label.value | strip %}

{% if label == blank %}
  {% if file != blank %}
    {% assign label = 'PDF herunterladen' %}
  {% else %}
    {% assign label = 'Zu den Schritten' %}
  {% endif %}
{% endif %}

{% if file != blank %}
  <a class="button" href="{{ file | file_url }}" target="_blank" rel="noopener">{{ label | escape }}</a>
{% else %}
  <a class="button" href="#diy-steps-anchor">{{ label | escape }}</a>
{% endif %}
'@

$heroButton.type = 'custom-liquid'
$heroButton.settings = @{ custom_liquid = $buttonLiquid }
$template.sections.section_Hca4zN.blocks.group_rjq9Lc.blocks.button_wEwTDT = $heroButton

# Validate JSON before pushing.
# PowerShell's ConvertTo-Json hard-limits serialization depth (max 100).
$fixed = $template | ConvertTo-Json -Depth 90 -Compress
$null = $fixed | ConvertFrom-Json -ErrorAction Stop

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 20
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  changed = $changed
  steps_anchor_added = ($stepsLiquid -match 'diy-steps-anchor')
  hero_button_is_custom_liquid = ($template.sections.section_Hca4zN.blocks.group_rjq9Lc.blocks.button_wEwTDT.type -eq 'custom-liquid')
} | ConvertTo-Json -Compress
