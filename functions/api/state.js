const DEFAULT_NEON_URL = "https://ep-withered-feather-b3n0w2vd.c-4.ap-southeast-1.aws.neon.tech/sql";
const DEFAULT_CONN_STR = "postgresql://neondb_owner:npg_a4uAMZfocK0I@ep-withered-feather-b3n0w2vd.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require";

const CORS_HEADERS = {
  "Content-Type": "application/json",
  "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
};

async function runSql(env, query, params = []) {
  const neonUrl = (env && env.NEON_HTTP_URL) || DEFAULT_NEON_URL;
  const connStr = (env && env.DATABASE_URL) || DEFAULT_CONN_STR;

  const resp = await fetch(neonUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Neon-Connection-String": connStr
    },
    body: JSON.stringify({ query, params })
  });

  if (!resp.ok) {
    const errText = await resp.text();
    throw new Error(`Neon SQL Error (${resp.status}): ${errText}`);
  }
  return await resp.json();
}

async function fetchCurrentState(env) {
  const res = await runSql(
    env,
    "SELECT key, value FROM app_settings WHERE key IN ('cover_overrides', 'date_overrides', 'favorites', 'bucket_list');"
  );

  const state = {
    cover_overrides: {},
    date_overrides: {},
    favorites: null,
    bucket_list: null
  };

  for (const row of (res.rows || [])) {
    try {
      state[row.key] = JSON.parse(row.value);
    } catch (_) {
      // Ignore malformed JSON
    }
  }
  return state;
}

async function upsertSetting(env, key, valObj) {
  const jsonStr = JSON.stringify(valObj);
  await runSql(
    env,
    "INSERT INTO app_settings (key, value) VALUES ($1, $2) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;",
    [key, jsonStr]
  );
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestGet(context) {
  try {
    const state = await fetchCurrentState(context.env);
    return new Response(JSON.stringify({ ok: true, ...state }), {
      status: 200,
      headers: CORS_HEADERS
    });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: err.message }), {
      status: 500,
      headers: CORS_HEADERS
    });
  }
}

export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const current = await fetchCurrentState(context.env);

    // 1. Merge cover_overrides if provided
    if (body.cover_overrides && typeof body.cover_overrides === "object") {
      const mergedCovers = { ...(current.cover_overrides || {}), ...body.cover_overrides };
      await upsertSetting(context.env, "cover_overrides", mergedCovers);
      current.cover_overrides = mergedCovers;
    }

    // 2. Merge date_overrides if provided
    if (body.date_overrides && typeof body.date_overrides === "object") {
      const mergedDates = { ...(current.date_overrides || {}), ...body.date_overrides };
      await upsertSetting(context.env, "date_overrides", mergedDates);
      current.date_overrides = mergedDates;
    }

    // 3. Save favorites array if provided
    if (Array.isArray(body.favorites)) {
      await upsertSetting(context.env, "favorites", body.favorites);
      current.favorites = body.favorites;
    }

    // 4. Save bucket_list array if provided
    if (Array.isArray(body.bucket_list)) {
      await upsertSetting(context.env, "bucket_list", body.bucket_list);
      current.bucket_list = body.bucket_list;
    }

    return new Response(JSON.stringify({ ok: true, ...current }), {
      status: 200,
      headers: CORS_HEADERS
    });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: err.message }), {
      status: 500,
      headers: CORS_HEADERS
    });
  }
}
