#!/usr/bin/env node

/**
 * Fetch Retool content pipeline artifacts (dossier, brief, article, products)
 * Usage:
 *   node fetch-retool-artifacts.js latest [topic-filter]
 *   node fetch-retool-artifacts.js <dossier-id>
 */

const pg = require('pg');

const DB_CONFIG = {
  host: 'ep-misty-wind-ak6qaapt-pooler.c-3.us-west-2.retooldb.com',
  port: 5432,
  user: 'retool',
  password: 'npg_nGJpXRcD2Mh5',
  database: 'retool',
  ssl: { rejectUnauthorized: false },
};

async function getTableColumns(client, tableName) {
  const res = await client.query(
    `SELECT column_name
     FROM information_schema.columns
     WHERE table_name = $1`,
    [tableName]
  );
  return new Set(res.rows.map(row => row.column_name));
}

async function fetchArtifacts(dossierId) {
  const client = new pg.Client(DB_CONFIG);
  
  try {
    await client.connect();
    console.error(`[fetch-retool-artifacts] Connected to Retool DB`);

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
    
    console.error(`[fetch-retool-artifacts] Found dossier: "${topic}" (${dossier.id})`);

    // 2. Fetch approved products for this keyword
    const productsQuery = `
      SELECT approval_id, keyword, product_handle, product_name, image_url, product_url, search_url, status, updated_at
      FROM product_keyword_approvals
      WHERE keyword = $1 AND status = 'Use Product Link'
      ORDER BY updated_at DESC
    `;
    
    const productsRes = await client.query(productsQuery, [topic]);
    console.error(`[fetch-retool-artifacts] Found ${productsRes.rows.length} approved products`);

    // 3. Attempt to fetch brief (if persisted)
    const briefQuery = `
      SELECT * FROM content_briefs
      WHERE primary_keyword = $1 OR primary_keyword = $2
      ORDER BY created_at DESC, id DESC
      LIMIT 1
    `;
    
    let brief = null;
    try {
      const briefRes = await client.query(briefQuery, [topic, dossier.id]);
      brief = briefRes.rows[0] || null;
    } catch (e) {
      console.error(`[fetch-retool-artifacts] content_briefs table not accessible (expected; briefs may not be persisted yet)`);
    }

    if (brief) {
      console.error(`[fetch-retool-artifacts] Found persisted brief`);
    }

    // 4. Attempt to fetch article (if persisted)
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
      console.error(`[fetch-retool-artifacts] staged_articles table not accessible (expected; articles may not be persisted yet)`);
    }

    if (article) {
      console.error(`[fetch-retool-artifacts] Found persisted article`);
    }

    // 5. Build output bundle
    const bundle = {
      dossier: {
        id: dossier.id,
        topic: topic,
        research_type: dossier.research_type,
        locale: dossier.locale,
        competitor_url: dossier.competitor_url,
        model: dossier.model,
        max_sources: dossier.max_sources,
        created_at: dossier.created_at,
        updated_at: dossier.updated_at,
      },
      research_json: dossier.result_json ? JSON.parse(dossier.result_json) : null,
      products: productsRes.rows.map(p => ({
        product_handle: p.product_handle,
        product_name: p.product_name,
        product_url: p.product_url,
        image_url: p.image_url,
        status: p.status,
      })),
      brief: brief ? {
        id: brief.id,
        title: brief.title,
        content: brief.brief_text || brief.content,
        created_at: brief.created_at,
      } : null,
      article: article ? {
        id: article.id,
        html: article.article_html || article.html,
        markdown: article.markdown || null,
        created_at: article.created_at,
      } : null,
    };

    console.error(`[fetch-retool-artifacts] Bundle ready (${Object.keys(bundle).length} artifacts)`);
    
    return bundle;

  } finally {
    await client.end();
  }
}

// Main
(async () => {
  try {
    const [, , arg1, arg2] = process.argv;
    
    let dossierId = null;
    
    if (arg1 === 'latest') {
      // Fetch latest dossier (optionally filtered by topic)
      dossierId = null;
    } else if (arg1) {
      dossierId = arg1;
    } else {
      console.error('Usage: fetch-retool-artifacts.js latest [topic-filter]');
      console.error('       fetch-retool-artifacts.js <dossier-id>');
      process.exit(1);
    }

    const bundle = await fetchArtifacts(dossierId);
    
    console.log(JSON.stringify(bundle, null, 2));
    
  } catch (err) {
    console.error(`[fetch-retool-artifacts] ERROR:`, err.message);
    process.exit(1);
  }
})();
