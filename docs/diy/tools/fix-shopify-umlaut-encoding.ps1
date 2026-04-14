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

function StrFromCodes([int[]]$codes) {
  $sb = New-Object System.Text.StringBuilder
  foreach ($c in $codes) { [void]$sb.Append([char]$c) }
  return $sb.ToString()
}

# Mojibake sequences (UTF-8 bytes interpreted as CP1252) built from char codes so this file stays ASCII.
$moj_ue = StrFromCodes @(0x00C3, 0x00BC) # "Ã¼"
$moj_Ue = StrFromCodes @(0x00C3, 0x009C) # "Ãœ"
$moj_ae = StrFromCodes @(0x00C3, 0x00A4) # "Ã¤"
$moj_Ae = StrFromCodes @(0x00C3, 0x0084) # "Ã„"
$moj_oe = StrFromCodes @(0x00C3, 0x00B6) # "Ã¶"
$moj_Oe = StrFromCodes @(0x00C3, 0x0096) # "Ã–"
$moj_sz = StrFromCodes @(0x00C3, 0x009F) # "ÃŸ"
$moj_eur = StrFromCodes @(0x00E2, 0x201A, 0x00AC) # "â‚¬"

# Target characters built from codepoints.
$ue = [string][char]0x00FC
$Ue = [string][char]0x00DC
$ae = [string][char]0x00E4
$Ae = [string][char]0x00C4
$oe = [string][char]0x00F6
$Oe = [string][char]0x00D6
$sz = [string][char]0x00DF
$eur = [string][char]0x20AC

function FixMojibake([string]$s) {
  if (-not $s) { return $s }
  return $s.
    Replace($moj_ue, $ue).Replace($moj_Ue, $Ue).
    Replace($moj_ae, $ae).Replace($moj_Ae, $Ae).
    Replace($moj_oe, $oe).Replace($moj_Oe, $Oe).
    Replace($moj_sz, $sz).
    Replace($moj_eur, $eur)
}

$assetKey = 'sections/master-diy-anleitung.liquid'
$encodedKey = [System.Uri]::EscapeDataString($assetKey)
$getUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json?asset[key]=' + $encodedKey

$orig = (Invoke-RestMethod -Uri $getUrl -Headers $headersGet -Method Get).asset.value
$fixed = FixMojibake $orig

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 20
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

$urls = @(
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj',
  'https://www.bastelschachtel.at/pages/diy-experience/diy-experience-y8igvhsi'
)

$pattern = [regex]::Escape($moj_ue) + '|' + [regex]::Escape($moj_ae) + '|' + [regex]::Escape($moj_oe) + '|' + [regex]::Escape($moj_eur)

$results = @()
foreach ($u in $urls) {
  $resp = Invoke-WebRequest -Uri $u -UseBasicParsing
  $ms = New-Object System.IO.MemoryStream
  $resp.RawContentStream.CopyTo($ms)
  $bytes = $ms.ToArray()
  $html = [Text.Encoding]::UTF8.GetString($bytes)
  $results += [pscustomobject]@{
    url = $u
    status = [int]$resp.StatusCode
    has_mojibake = ($html -match $pattern)
  }
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  changed = $changed
  checks = $results
} | ConvertTo-Json -Compress
