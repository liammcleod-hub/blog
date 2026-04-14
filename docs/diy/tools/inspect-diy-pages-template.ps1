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

$headers = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }
$endpoint = 'https://' + $shopDomain + '/admin/api/2025-01/graphql.json'

$query = @'
query($q: String!) {
  pages(first: 1, query: $q) {
    nodes {
      id
      handle
      title
      templateSuffix
    }
  }
}
'@

function FetchPage([string]$handle) {
  $q = 'handle:' + $handle
  $body = @{ query = $query; variables = @{ q = $q } } | ConvertTo-Json -Compress -Depth 10
  $resp = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Body $body
  [pscustomobject]@{
    handle = $handle
    page = @($resp.data.pages.nodes)[0]
    errors = $resp.errors
  }
}

@(
  FetchPage 'diy-experience-8jsy7ngj'
  FetchPage 'diy-experience-y8igvhsi'
) | ConvertTo-Json -Compress -Depth 20
