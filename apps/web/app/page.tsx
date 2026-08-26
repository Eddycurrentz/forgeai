const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

type HealthResponse = {
  status: string;
  service: string;
  environment: string;
  postgres: boolean;
  redis: boolean;
  version: string;
};

async function loadHealth(): Promise<HealthResponse | null> {
  try {
    const response = await fetch(`${apiUrl}/health`, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as HealthResponse;
  } catch {
    return null;
  }
}

export default async function HomePage() {
  const health = await loadHealth();

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-6 px-6">
      <p className="text-sm uppercase tracking-[0.2em] text-cyan-400">Phase 1 foundation</p>
      <h1 className="text-4xl font-semibold tracking-tight">ForgeAI</h1>
      <p className="text-slate-400">
        Operator console for the autonomous software engineer. This page only reports API
        and dependency health.
      </p>
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-6">
        {health ? (
          <dl className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <dt className="text-slate-500">API</dt>
              <dd className="font-medium">{health.status}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Version</dt>
              <dd className="font-medium">{health.version}</dd>
            </div>
            <div>
              <dt className="text-slate-500">PostgreSQL</dt>
              <dd className="font-medium">{health.postgres ? "connected" : "unavailable"}</dd>
            </div>
            <div>
              <dt className="text-slate-500">Redis</dt>
              <dd className="font-medium">{health.redis ? "connected" : "unavailable"}</dd>
            </div>
          </dl>
        ) : (
          <p className="text-amber-300">
            API is unreachable at <code className="text-amber-100">{apiUrl}</code>. Start the
            API, then refresh.
          </p>
        )}
      </section>
    </main>
  );
}
