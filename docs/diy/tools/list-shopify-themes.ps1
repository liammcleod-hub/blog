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
$url = 'https://' + $shopDomain + '/admin/api/2025-01/themes.json?fields=id,name,role,updated_at,previewable'
$resp = Invoke-RestMethod -Uri $url -Headers $headers -Method Get

$themes = @($resp.themes) | Sort-Object -Property updated_at -Descending
$themes | Select-Object id,name,role,updated_at,previewable | ConvertTo-Json -Compress

