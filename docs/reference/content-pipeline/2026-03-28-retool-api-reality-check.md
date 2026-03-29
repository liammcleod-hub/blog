You’re asking for exact live, read-only HTTP API adapter details (base URL, auth header, live endpoint paths, response shapes, and “known-good” verification IDs) for the Bastelschachtel content pipeline.

Based on the current Retool app code in this repo, there is no live read-only “content pipeline API” exposed as HTTP endpoints that a local plugin could call directly.

What does exist “live” today is:

Internal Retool Database tables (queried server-side by Retool via SQL / RetoolTableQuery), and
Outbound OpenRouter calls (Retool → OpenRouter) for LLM research/generation.
That means: there is no base URL / auth header / endpoint map for a Bastelschachtel “content pipeline API” in the current implementation.

Below is the most precise, implementation-ready “truth” I can give from the repo, separated into LIVE NOW vs NOT LIVE / PLANNED.

0) Status: Is there a live read-only HTTP API for the plugin?
Not live.

There are no RESTQuery / OpenAPIQuery definitions that expose your “content pipeline” as an HTTP server.
Retool queries here are clients of:
Retool Database (SQL)
OpenRouter (REST)
Google Docs (OpenAPIQuery)
A local plugin can’t directly “call into Retool queries” unless you separately build/deploy an API layer (Retool Workflows as API, Retool RPC, a separate service, etc.).

1) Base URL (for the plugin to call)
Bastelschachtel content pipeline API
Not live → no base URL exists in this codebase.

What base URLs exist in practice (outbound dependencies)
These are not plugin-callable “content pipeline endpoints”; they are services Retool calls.

OpenRouter resource is used with relative paths:

POST /chat/completions
GET /models
However, the actual OpenRouter base URL is configured in the Retool Resource (OpenRouter_API) and is not present in this repo. (Retool resources store base URLs/secrets outside the app source.)

Google Docs API (Brand Guidelines doc fetch) is called via OpenAPIQuery:

GET /v1/documents/{documentId}
Again, the Google API base URL is resource-level configuration, not in the repo.

2) Authentication (read-only requests)
Bastelschachtel content pipeline API
Not live → no auth method / header / token format exists to provide.

What auth exists (outbound dependencies)
OpenRouter auth is configured on the Retool resource OpenRouter_API and is not visible in the repo, so I cannot truthfully provide:

header name
token format example
whether token is shared across endpoints
Google Docs auth is configured on the Retool resource Bastelschachtel Brand Guidelines and is not visible in the repo.

Retool Database queries authenticate implicitly via Retool’s server-side resource connection; there is no HTTP token because this isn’t an HTTP API.

3) Live endpoint map (HTTP)
Bastelschachtel “content pipeline” endpoints you requested
All of these are NOT LIVE as HTTP endpoints in the current repo:

latest keyword lookup → not live
get research dossier by id → not live
list research dossiers by topic → not live
get approved products by keyword → not live
get products by handles → not live
optional topic facts by topic → not live
What is live as HTTP calls (Retool → external)
These are outbound calls, not your plugin calling in:

Purpose	Method	Path	Params	Live now?
LLM chat completions (Research Lab)	POST	/chat/completions	body = bodyOverride	Yes (Retool → OpenRouter)
LLM chat completions (Content Factory)	POST	/chat/completions	body = bodyOverrideContentFactory	Yes (Retool → OpenRouter)
OpenRouter model list	GET	/models	none	Yes (Retool → OpenRouter)
Fetch Brand Guidelines Google Doc	GET	/v1/documents/{documentId}	documentId=18qK8i9_YNY5-Vik4tzLlm_r_pKTIiZbD1t_Lshzp8VY	Yes (Retool → Google Docs)
4) Response shapes (for “live endpoints”)
Since the Bastelschachtel content pipeline HTTP endpoints are not live, there are no HTTP response shapes I can provide for those.

What I can give precisely is the data shapes that exist in the Retool Database queries, because those are the “source of truth” your eventual API would likely wrap.

4.1 Research dossiers (DB shape used throughout the app)
Query: listResearchDossiers.sql / listResearchDossiersGlobal.sql

Columns returned:

id,
topic,
research_type,
competitor_url,
locale,
model,
max_sources,
status,
created_at,
updated_at,
result_json
Critical detail you asked about (“where dossier JSON lives”):

The app normalizes the dossier JSON into a field named result_json.
It is derived as
  COALESCE(NULLIF(result_json,''), dossier_json) AS result_json
meaning:

preferred: result_json
fallback: legacy dossier_json
So: today, the dossier JSON is accessed as result_json in the app’s normalized layer.

Keyword vs topic naming:

The normalized field exposed is topic
It is derived as:
COALESCE(NULLIF(topic,''), keyword) AS topic
So: today the “topic/keyword” value is exposed as topic by the listing queries.

ID field naming:

The dossier id column is id (returned as id)
4.2 Approved products by keyword (DB shape)
Query: listProductKeywordApprovals.sql

Columns returned:

sql
approval_id,
keyword,
product_handle,
product_name,
image_url,
product_url,
search_url,
status,
updated_at


So: approvals are keyed by:
- `keyword` (string)
- products are in `product_handle`, `product_name`, `image_url`, `product_url`
- status values include **`Use Product Link`** (this is explicitly used in JS logic)

### 4.3 Product catalog search (DB shape)
Query: `searchProductCatalog.sql` returns `SELECT * FROM product_catalog ... LIMIT 50;`

Because it’s `SELECT *`, the exact fields depend on the DB schema, but the app code expects at least:

- `id`
- `handle`
- `title`
- `display_title`
- `tags`
- `type`
- `vendor`
- `variant_sku`
- `variant_price_cents`
- `image_src`
- `image_alt_text`
- `canonical_id_url`

(Those appear explicitly in `listProductCatalog.sql` and in mapping code.)

### 4.4 Product facts by topic (DB shape)
Query: `listProductFacts.sql`

**Columns returned:**
sql
id,
topic,
fact_text,
source_url,
category,
created_at


Filter behavior:
- If `selectedDossierTopic` is not set, returns all facts.
- Else `WHERE topic = selectedDossierTopic`.

---

## 5) “Real verification examples” (known-good id/topic/keyword)
I **cannot provide real, currently-valid IDs/topics/keywords** from the live system because:

- This repo contains **query definitions**, but **no live database contents**.
- In Ask mode, I also can’t run queries against your Retool DB to fetch an actual dossier id/topic/keyword.

So these are **not available from source code alone**:
- a real dossier id that resolves successfully
- a real topic value that returns dossier data
- a real keyword that returns product approvals

If you want, I can tell you *exactly how to obtain them* from within Retool UI right now (manual verification steps), but I can’t invent “real IDs” without access to the environment data.

---

## 6) Stability notes (what’s safe for a client to depend on)
Because there is **no live HTTP API contract**, the only “stable” contract is what the app itself uses internally:

### Stable enough (based on code usage)
If you build a read-only API wrapper around the DB, these are the fields the app already depends on:

**Research dossiers**
- `id` (string/text)
- `topic` (string) — normalized from `topic`/`keyword`
- `research_type`
- `result_json` (string containing JSON)

**Approvals**
- `keyword`
- `product_handle`
- `product_name`
- `image_url`
- `product_url`
- `status` (the app checks specifically for `'Use Product Link'`)

**Product catalog**
- `handle`, `title`/`display_title`, `image_src`, `variant_price_cents`, etc.

### Likely to change / already “compatibility-layered”
- Dossier JSON column naming is **already migrated/dual** (`result_json` vs legacy `dossier_json`)
- Topic naming is **already dual** (`topic` vs legacy `keyword`)

That’s a strong signal that any client should treat:
- `topic` and `result_json` as **canonical output fields** of an API,
- but assume the backend may still be in transition internally.

### Recommended normalization layer for a plugin
If/when you expose an API, normalize at the boundary:
- Always output `topic` (never `keyword`)
- Always output `result_json` (never `dossier_json`)
- Always output `id` (never `dossier_id`)
- For products, output `product_handle` and `product_url` consistently

---

## 7) Safe client recommendation (best read-only plugin contract)
Since **nothing is live as HTTP**, the safest recommendation is:

### Canonical data sources (today)
- **research_dossiers** (read-only)
- **product_keyword_approvals** (read-only)
- **product_catalog** (read-only)
- **product_facts** (read-only)

### Canonical “API” endpoints (recommended to implement; NOT LIVE today)
Marking these explicitly as **PLANNED / NOT LIVE**:

1) **Latest keyword lookup**  
   - NOT LIVE  
   - Suggested: `GET /keywords/latest` (or derive from `keyword_data` / most recent dossier)

2) **Get research dossier by id**  
   - NOT LIVE  
   - Suggested: `GET /research-dossiers/{id}`  
   - Required fields: `id`, `topic`, `research_type`, `result_json`, timestamps

3) **List dossiers by topic**  
   - NOT LIVE  
   - Suggested: `GET /research-dossiers?topic=...`

4) **Get approved products by keyword**  
   - NOT LIVE  
   - Suggested: `GET /product-approvals?keyword=...`  
   - Required: `keyword`, `products[]` with `product_handle`, `product_name`, `product_url`, `image_url`, `status`

5) **Get products by handles**  
   - NOT LIVE  
   - Suggested: `POST /products/by-handles` with JSON body `{ handles: string[] }`  
     (avoid long querystrings)

6) **Optional topic facts by topic**  
   - NOT LIVE  
   - Suggested: `GET /product-facts?topic=...`

### Rate limits / auth caveats
- There are **no documented rate limits** for a non-existent API.
- If you decide to wrap Retool DB with an API:
  - Add caching headers for read-only responses (`ETag` / `Last-Modified`) if feasible.
  - Implement a conservative default limit (e.g. 60 req/min per token) unless you know your plugin’s call frequency.

---

# What you likely need next (so I can give you the “exact live” details you asked for)
To provide the **exact base URL, auth headers, live endpoint map, exact response JSON**, we need one of these to exist:

1) A deployed **HTTP API service** (Retool Workflows “API”, Retool authenticated REST endpoints, or external server) that exposes the pipeline data, **or**
2) A clear statement that the plugin should call **Retool Database directly** (rare/unrecommended), **or**
3) You share the **actual API adapter implementation** (paths/routes) if it exists elsewhere (another repo/service).

If you tell me **where the plugin is supposed to call** (Retool Workflow URL? internal gateway? localhost adapter?), I can produce the exact implementation-ready contract.

---

## Summary (live facts from this repo)
- **No live Bastelschachtel content pipeline HTTP API exists** in the current Retool app source → base URL/auth/endpoints for the plugin are **not available**.
- The “truth” today is **Retool Database tables** and internal normalization:
  - dossiers: `id`, `topic`, `research_type`, **`result_json`**
  - approvals: `keyword`, `product_handle`, etc.
  - products: `product_catalog` rows
  - facts: `product_facts` rows

## Next steps (pick one)
1) Tell me **where the plugin should connect** (Workflow API? existing gateway?), and I’ll map **exact endpoints + auth**.
2) If you want this app to *be* the API: switch to **Build mode**, and we can add a **read-only API layer** (most commonly: Retool Workflows with authenticated GET endpoints) that exposes the exact endpoints you listed.