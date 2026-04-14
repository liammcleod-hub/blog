param(
  [string[]]$Types = @('product_faq', 'diy_experience')
)

$ErrorActionPreference = 'Stop'

$envFile = 'C:\Users\Hp\Documents\anothervault\01-Projects\Vektal\Code\.env'
$shopDomain = ''
$token = ''
Get-Content -LiteralPath $envFile | ForEach-Object {
  if ($_ -match '^SHOP_DOMAIN=(.*)$') { $shopDomain = $matches[1] }
  elseif ($_ -match '^SHOPIFY_ACCESS_TOKEN=(.*)$') { $token = $matches[1] }
}
if (-not $shopDomain -or -not $token) { throw "Missing SHOP_DOMAIN / SHOPIFY_ACCESS_TOKEN in $envFile" }

$endpoint = 'https://' + $shopDomain + '/admin/api/2025-01/graphql.json'
$headers = @{ 'X-Shopify-Access-Token' = $token; 'Content-Type' = 'application/json' }

$query = @'
query($after: String) {
  metaobjectDefinitions(first: 250, after: $after) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      type
      name
      displayNameKey
      fieldDefinitions {
        key
        name
        required
        description
        type { name category }
      }
    }
  }
}
'@

$defs = @()
$after = $null
for ($i = 0; $i -lt 20; $i++) {
  $body = @{ query = $query; variables = @{ after = $after } } | ConvertTo-Json -Compress -Depth 20
  $resp = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Body $body
  if ($resp.errors) { throw ($resp.errors | ConvertTo-Json -Compress -Depth 20) }
  $page = $resp.data.metaobjectDefinitions
  $defs += @($page.nodes)
  if (-not $page.pageInfo.hasNextPage) { break }
  $after = $page.pageInfo.endCursor
}

$defs = @($defs) | Where-Object { $Types -contains $_.type }

[pscustomobject]@{
  shop = $shopDomain
  types = $Types
  found = @($defs | ForEach-Object {
    [pscustomobject]@{
      type = $_.type
      name = $_.name
      displayNameKey = $_.displayNameKey
      fields = @($_.fieldDefinitions | Select-Object key,name,required,@{n='type_name';e={$_.type.name}},@{n='type_category';e={$_.type.category}})
    }
  })
} | ConvertTo-Json -Compress -Depth 30
