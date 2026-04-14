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

# Find the nested group block that contains the materials grid block.
$targetSectionKey = $null
$targetGroupPath = @() # e.g. group_8RBniT, group_phhc36
foreach ($k in $template.sections.PSObject.Properties.Name) {
  $sec = $template.sections.$k
  if ($null -eq $sec.blocks) { continue }

  # DFS over nested groups.
  $stack = New-Object System.Collections.Stack
  foreach ($bk in @($sec.blocks.PSObject.Properties.Name)) {
    $b = $sec.blocks.$bk
    if ($b.type -eq 'group') {
      $stack.Push(@($bk, $b))
    }
  }

  while ($stack.Count -gt 0) {
    $item = $stack.Pop()
    $path = @($item[0])
    $grp = $item[1]

    # Track full path by embedding it in the group object for traversal.
    if ($grp.PSObject.Properties.Name -contains '__path') {
      $path = @($grp.__path) + @($path)
    }

    $innerKeys = @()
    if ($null -ne $grp.blocks) { $innerKeys = @($grp.blocks.PSObject.Properties.Name) }
    if ($innerKeys -contains 'custom_liquid_materials_grid') {
      $targetSectionKey = $k
      $targetGroupPath = $path
      break
    }

    # Push child groups.
    foreach ($ck in $innerKeys) {
      $child = $grp.blocks.$ck
      if ($child.type -eq 'group') {
        # Store accumulated path on the child for retrieval.
        $child | Add-Member -MemberType NoteProperty -Name '__path' -Value $path -Force
        $stack.Push(@($ck, $child))
      }
    }
  }

  if ($targetSectionKey) { break }
}

if (-not $targetSectionKey -or $targetGroupPath.Count -eq 0) {
  throw "Could not find nested group containing block 'custom_liquid_materials_grid' in $assetKey"
}

$secObj = $template.sections.$targetSectionKey

$groupObj = $secObj.blocks.$($targetGroupPath[0])
for ($pi = 1; $pi -lt $targetGroupPath.Count; $pi++) {
  $groupObj = $groupObj.blocks.$($targetGroupPath[$pi])
}

if ($null -eq $groupObj.blocks) { $groupObj | Add-Member -MemberType NoteProperty -Name blocks -Value (@{}) -Force }
if ($null -eq $groupObj.block_order) { $groupObj | Add-Member -MemberType NoteProperty -Name block_order -Value (@()) -Force }

$blockKey = 'custom_liquid_faq'
if (-not ($groupObj.blocks.PSObject.Properties.Name -contains $blockKey)) {
  $faqLiquid = @'
<div id="diy-faq-{{ block.id }}" class="diy-faq">
  <style>
    #diy-faq-{{ block.id }} {
      padding: 36px 0;
    }
    #diy-faq-{{ block.id }} .diy-faq__wrap {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 16px;
    }
    #diy-faq-{{ block.id }} .diy-faq__title {
      margin: 0 0 14px;
      font-weight: 800;
      letter-spacing: -0.01em;
    }
    #diy-faq-{{ block.id }} .diy-faq__lead {
      margin: 0 0 18px;
      color: rgba(0,0,0,0.7);
    }
    #diy-faq-{{ block.id }} .diy-faq__item {
      border: 1px solid #eee;
      border-radius: 12px;
      background: #fff;
      padding: 0;
      overflow: hidden;
    }
    #diy-faq-{{ block.id }} .diy-faq__item + .diy-faq__item { margin-top: 10px; }
    #diy-faq-{{ block.id }} summary {
      cursor: pointer;
      list-style: none;
      padding: 14px 16px;
      font-weight: 700;
    }
    #diy-faq-{{ block.id }} summary::-webkit-details-marker { display: none; }
    #diy-faq-{{ block.id }} .diy-faq__answer {
      padding: 0 16px 14px;
      color: rgba(0,0,0,0.85);
      line-height: 1.5;
    }
  </style>

  {% assign diy = closest.metaobject.diy_experience %}
  {% assign faqs = diy.faq_items.value %}

  {% if faqs != blank %}
    <div class="diy-faq__wrap">
      <h2 class="diy-faq__title">H&auml;ufige Fragen</h2>

      {% for faq in faqs %}
        {% assign q = faq.question.value | strip %}
        {% assign a = faq.answer.value | strip %}

        {% if q != blank and a != blank %}
          <details class="diy-faq__item">
            <summary>{{ q | escape }}</summary>
            <div class="diy-faq__answer">{{ a | escape | newline_to_br }}</div>
          </details>
        {% endif %}
      {% endfor %}
    </div>

    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
          {% assign first = true %}
          {% for faq in faqs %}
            {% assign q = faq.question.value | strip %}
            {% assign a = faq.answer.value | strip %}
            {% if q != blank and a != blank %}
              {% unless first %},{% endunless %}
              {
                "@type": "Question",
                "name": {{ q | json }},
                "acceptedAnswer": {
                  "@type": "Answer",
                  "text": {{ a | json }}
                }
              }
              {% assign first = false %}
            {% endif %}
          {% endfor %}
        ]
      }
    </script>
  {% endif %}
</div>
'@

  $groupObj.blocks | Add-Member -MemberType NoteProperty -Name $blockKey -Value ([pscustomobject]@{
    type = 'custom-liquid'
    settings = @{
      custom_liquid = $faqLiquid
    }
  }) -Force

  # Insert after materials grid block if possible; else append.
  $order = @($groupObj.block_order)
  if ($order -contains 'custom_liquid_materials_grid') {
    $idx = [Array]::IndexOf($order, 'custom_liquid_materials_grid')
    if ($idx -ge 0) {
      $before = @()
      if ($idx -ge 0) { $before = $order[0..$idx] }
      $after = @()
      if ($idx + 1 -le $order.Length - 1) { $after = $order[($idx + 1)..($order.Length - 1)] }
      $groupObj.block_order = @($before + @($blockKey) + $after)
    } else {
      $groupObj.block_order = @($order + @($blockKey))
    }
  } else {
    $groupObj.block_order = @($order + @($blockKey))
  }
}

$fixed = $template | ConvertTo-Json -Depth 80 -Compress

$changed = $false
if ($fixed -ne $orig) {
  $putUrl = 'https://' + $shopDomain + '/admin/api/2025-01/themes/' + $themeId + '/assets.json'
  $body = @{ asset = @{ key = $assetKey; value = $fixed } } | ConvertTo-Json -Compress -Depth 100
  Invoke-RestMethod -Uri $putUrl -Headers $headersPut -Method Put -Body $body | Out-Null
  $changed = $true
}

[pscustomobject]@{
  theme_id = $themeId
  asset = $assetKey
  target_section = $targetSectionKey
  target_group_path = $targetGroupPath
  added_block = $blockKey
  changed = $changed
} | ConvertTo-Json -Compress
