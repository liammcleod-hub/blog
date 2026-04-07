#!/usr/bin/env node

/**
 * Create a blog-seo-pipeline job folder with artifacts fetched from Retool DB
 * 
 * Usage:
 *   node create-blog-job-from-retool.js latest
 *   node create-blog-job-from-retool.js <dossier-id>
 *   node create-blog-job-from-retool.js latest --brief --article
 * 
 * Creates:
 *   output/content-jobs/<job-slug>/
 *     ├── job.json (metadata)
 *     ├── research-dossier.json
 *     ├── selected-products.json
 *     ├── brief.md (if --brief or if persisted)
 *     └── article.html (if --article or if persisted)
 */

const pg = require('pg');
const path = require('path');
const fs = require('fs');

const DB_CONFIG = {
  host: 'ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com',
  port: 5432,
  user: 'retool',
  password: 'npg_nGJpXRcD2Mh5',
  database: 'retool',
  ssl: { rejectUnauthorized: false },
};

const OUTPUT_BASE = path.join(__dirname, '../../output/content-jobs');

async function getTableColumns(client, tableName) {
  const res = await client.query(
    `SELECT column_name
     FROM information_schema.columns
     WHERE table_name = $1`,
    [tableName]
  );
  return new Set(res.rows.map(row => row.column_name));
}

function slugify(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]/g, '')
    .replace(/\-+/g, '-')
    .replace(/^\-|\-$/g, '');
}

async function fetchArtifacts(dossierId) {
  const client = new pg.Client(DB_CONFIG);
  
  try {
    await client.connect();
    console.error(`[create-job] Connected to Retool DB`);

    // 1. Fetch research dossier
    const dossierQuery = dossierId 
      ? 'SELECT * FROM research_dossiers WHERE id = $1'
      : `SELECT * FROM research_dossiers 
         WHERE status != 'archived' 
         ORDER BY created_at DESC 
         LIMIT 1`;
    
    const dossierParams = dossierId ? [dossierId] : [];
    const dossierRes = await client.query(dossierQuery, dossierParams);
    
    if (dossierRes.rows.length === 0) {
      throw new Error(dossierId 
        ? `Dossier ${dossierId} not found` 
        : 'No recent dossier found');
    }

    const dossier = dossierRes.rows[0];
    const topic = dossier.topic || dossier.keyword;
    
    console.error(`[create-job] Found dossier: "${topic}" (id: ${dossier.id})`);

    // 2. Fetch approved products for this keyword
    const productsQuery = `
      SELECT approval_id, keyword, product_handle, product_name, image_url, product_url, search_url, status, updated_at
      FROM product_keyword_approvals
      WHERE keyword = $1 AND status = 'Use Product Link'
      ORDER BY updated_at DESC
    `;
    
    const productsRes = await client.query(productsQuery, [topic]);
    console.error(`[create-job] Found ${productsRes.rows.length} approved products`);

    // 3. Attempt to fetch brief
    let brief = null;
    const briefQuery = `
      SELECT * FROM content_briefs
      WHERE primary_keyword = $1 OR primary_keyword ILIKE $2
      ORDER BY created_at DESC, id DESC
      LIMIT 1
    `;
    
    try {
      const briefRes = await client.query(briefQuery, [topic, `%${topic}%`]);
      brief = briefRes.rows[0] || null;
    } catch (e) {
      // Table may not exist or be inaccessible
    }

    if (brief) {
      console.error(`[create-job] Found persisted brief`);
    }

    // 4. Attempt to fetch article
    let article = null;

    try {
      const articleColumns = await getTableColumns(client, 'staged_articles');
      const dossierColumn = articleColumns.has('research_dossier_id')
        ? 'research_dossier_id'
        : articleColumns.has('dossier_id')
          ? 'dossier_id'
          : null;
      const keywordColumn = articleColumns.has('primary_keyword')
        ? 'primary_keyword'
        : articleColumns.has('keyword')
          ? 'keyword'
          : null;

      const filters = [];
      const params = [];

      if (dossierColumn) {
        params.push(dossier.id);
        filters.push(`${dossierColumn} = $${params.length}`);
      }
      if (keywordColumn) {
        params.push(`%${topic}%`);
        filters.push(`${keywordColumn} ILIKE $${params.length}`);
      }

      if (filters.length > 0) {
        const articleQuery = `
          SELECT * FROM staged_articles
          WHERE ${filters.join(' OR ')}
          ORDER BY updated_at DESC NULLS LAST, created_at DESC, id DESC
          LIMIT 1
        `;

        const articleRes = await client.query(articleQuery, params);
        article = articleRes.rows[0] || null;
      }
    } catch (e) {
      // Table may not exist or be inaccessible
    }

    if (article) {
      console.error(`[create-job] Found persisted article`);
    }

    return {
      dossier,
      topic,
      research_json: dossier.result_json ? JSON.parse(dossier.result_json) : null,
      products: productsRes.rows.map(p => ({
        product_handle: p.product_handle,
        product_name: p.product_name,
        product_url: p.product_url,
        image_url: p.image_url,
        status: p.status,
      })),
      brief,
      article,
    };

  } finally {
    await client.end();
  }
}

function getArticleContent(article) {
  if (!article) {
    return '';
  }
  return article.article_html || article.html || '';
}

async function createJobFolder(artifacts, options = {}) {
  const jobSlug = `${slugify(artifacts.topic)}-${new Date().toISOString().split('T')[0]}`;
  const jobDir = path.join(OUTPUT_BASE, jobSlug);
  
  // Create directory
  if (!fs.existsSync(jobDir)) {
    fs.mkdirSync(jobDir, { recursive: true });
    console.error(`[create-job] Created folder: ${jobDir}`);
  }

  // 1. Write job.json (metadata)
  const jobJson = {
    slug: jobSlug,
    topic: artifacts.topic,
    dossier_id: artifacts.dossier.id,
    research_type: artifacts.dossier.research_type,
    locale: artifacts.dossier.locale,
    created_at: new Date().toISOString(),
    created_from_retool: true,
  };

  fs.writeFileSync(
    path.join(jobDir, 'job.json'),
    JSON.stringify(jobJson, null, 2)
  );
  console.error(`[create-job] Wrote job.json`);

  // 2. Write research-dossier.json
  fs.writeFileSync(
    path.join(jobDir, 'research-dossier.json'),
    JSON.stringify(artifacts.research_json, null, 2)
  );
  console.error(`[create-job] Wrote research-dossier.json`);

  // 3. Write selected-products.json
  fs.writeFileSync(
    path.join(jobDir, 'selected-products.json'),
    JSON.stringify(artifacts.products, null, 2)
  );
  console.error(`[create-job] Wrote selected-products.json (${artifacts.products.length} products)`);

  // 4. Write brief.md (if available)
  if (artifacts.brief) {
    const briefContent = artifacts.brief.brief_text || artifacts.brief.content || '';
    fs.writeFileSync(
      path.join(jobDir, 'brief.md'),
      briefContent
    );
    console.error(`[create-job] Wrote brief.md`);
  } else if (options.expectBrief) {
    console.error(`[create-job] Warning: brief expected but not found in DB`);
  }

  // 5. Write article.html (if available)
  if (artifacts.article) {
    const articleContent = getArticleContent(artifacts.article);
    fs.writeFileSync(
      path.join(jobDir, 'article.html'),
      articleContent
    );
    console.error(`[create-job] Wrote article.html`);
  } else if (options.expectArticle) {
    console.error(`[create-job] Warning: article expected but not found in DB`);
  }

  // Output result
  console.log(JSON.stringify({
    success: true,
    job_folder: jobDir,
    job_slug: jobSlug,
    topic: artifacts.topic,
    dossier_id: artifacts.dossier.id,
    products_count: artifacts.products.length,
    has_brief: !!artifacts.brief,
    has_article: !!artifacts.article,
    files_created: [
      'job.json',
      'research-dossier.json',
      'selected-products.json',
      artifacts.brief ? 'brief.md' : null,
      artifacts.article ? 'article.html' : null,
    ].filter(Boolean),
  }, null, 2));
}

// Main
(async () => {
  try {
    const [, , arg1, ...otherArgs] = process.argv;
    
    if (!arg1 || arg1 === '--help' || arg1 === '-h') {
      console.log(`Usage: create-blog-job-from-retool.js latest [options]
       create-blog-job-from-retool.js <dossier-id> [options]

Options:
  --brief     Expect brief to be persisted (warn if not found)
  --article   Expect article to be persisted (warn if not found)
  --help      Show this help
`);
      process.exit(0);
    }

    const dossierId = arg1 === 'latest' ? null : arg1;
    const options = {
      expectBrief: otherArgs.includes('--brief'),
      expectArticle: otherArgs.includes('--article'),
    };

    const artifacts = await fetchArtifacts(dossierId);
    await createJobFolder(artifacts, options);
    
  } catch (err) {
    console.error(`[create-job] ERROR:`, err.message);
    console.log(JSON.stringify({ success: false, error: err.message }));
    process.exit(1);
  }
})();
