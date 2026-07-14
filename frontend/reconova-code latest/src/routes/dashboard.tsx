import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CookieNotice } from "@/components/CookieNotice";
import { Button } from "@/components/ui/button";
import { getSession } from "@/lib/auth";
import { PARSERS, activityByUser, seedActivity } from "@/lib/activity";
import { listUsers, seedIfEmpty } from "@/lib/auth";
import { Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Play, TrendingUp, Activity as ActivityIcon, Package } from "lucide-react";

export const Route = createFileRoute("/dashboard")({
  component: Dashboard,
  head: () => ({ meta: [{ title: "Dashboard — Reconova" }] }),
});

const CHART_COLORS = ["#2563EB", "#0891B2", "#059669", "#D97706", "#DC2626", "#7C3AED", "#DB2777"];

function Dashboard() {
  const nav = useNavigate();
  const [session, setSession] = useState<ReturnType<typeof getSession>>(null);

  useEffect(() => {
    seedIfEmpty();
    const s = getSession();
    if (!s) { nav({ to: "/login" }); return; }
    if (s.role === "admin") { nav({ to: "/admin" }); return; }
    seedActivity(listUsers().map(u => ({ id: u.id, email: u.email })));
    setSession(s);
  }, [nav]);

  const events = useMemo(() => session ? activityByUser(session.id) : [], [session]);

  const byParser = useMemo(() => {
    const map = new Map<string, number>();
    PARSERS.forEach(p => map.set(p, 0));
    events.forEach(e => map.set(e.parser, (map.get(e.parser) || 0) + 1));
    return Array.from(map, ([name, count]) => ({ name, count }));
  }, [events]);

  const byDay = useMemo(() => {
    const days: Record<string, number> = {};
    for (let i = 6; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days[d.toISOString().slice(0, 10)] = 0;
    }
    events.forEach(e => {
      const k = e.timestamp.slice(0, 10);
      if (k in days) days[k]++;
    });
    return Object.entries(days).map(([date, count]) => ({ date: date.slice(5), count }));
  }, [events]);


  if (!session) return null;

  const total = events.length;
  const uniqueParsers = new Set(events.map(e => e.parser)).size;
  const last7 = byDay.reduce((s, d) => s + d.count, 0);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-7xl px-6 py-10">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">Hey {session.name} 👋</h1>
            <p className="mt-1 text-muted-foreground">Here's what's happening with your parsers today.</p>
          </div>
          <span className="rounded-full bg-accent px-3 py-1 text-xs font-medium text-primary">User dashboard</span>
        </div>

        {/* Stats */}
        <div className="mt-8 grid gap-4 md:grid-cols-4">
          <StatCard icon={ActivityIcon} label="Total runs" value={total} />
          <StatCard icon={TrendingUp} label="Runs (last 7 days)" value={last7} />
          <StatCard icon={Package} label="Parsers used" value={uniqueParsers} />
          <StatCard icon={Play} label="Available parsers" value={PARSERS.length} />
        </div>

        {/* Parser grid */}
        <div className="mt-10">
          <h2 className="text-xl font-semibold">Your parsers</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {PARSERS.map((p, i) => {
              const count = byParser.find(x => x.name === p)?.count || 0;
              return (
                <div key={p} className="rounded-2xl border border-border bg-card p-5 shadow-sm transition hover:shadow-soft">
                  <div className="flex items-center justify-between">
                    <div className="grid h-10 w-10 place-items-center rounded-lg text-white" style={{ background: CHART_COLORS[i % CHART_COLORS.length] }}>
                      {p[0]}
                    </div>
                    <span className="text-xs text-muted-foreground">Used {count}×</span>
                  </div>
                  <h3 className="mt-4 font-semibold">{p}</h3>
                  <p className="mt-1 text-xs text-muted-foreground">Parse & reconcile {p} orders and payouts.</p>
                  <Link to="/parser/$name" params={{ name: p }}>
                    <Button size="sm" className="mt-4 w-full bg-gradient-brand text-white">
                      <Play className="mr-1 h-3.5 w-3.5" /> Open parser
                    </Button>
                  </Link>
                </div>
              );
            })}
          </div>
        </div>

        {/* Charts */}
        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <ChartCard title="Usage by parser" subtitle="How often you use each parser">
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={byParser}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 16% 90%)" />
                <XAxis dataKey="name" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip contentStyle={{ borderRadius: 8, border: "1px solid hsl(215 16% 90%)" }} />
                <Bar dataKey="count" radius={[8,8,0,0]}>
                  {byParser.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          <ChartCard title="Activity (last 7 days)" subtitle="Daily parser runs">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={byDay}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(215 16% 90%)" />
                <XAxis dataKey="date" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip contentStyle={{ borderRadius: 8, border: "1px solid hsl(215 16% 90%)" }} />
                <Line type="monotone" dataKey="count" stroke="#2563EB" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Recent activity */}
        <div className="mt-10 rounded-2xl border border-border bg-card shadow-sm">
          <div className="border-b border-border p-5">
            <h2 className="text-lg font-semibold">Recent activity</h2>
            <p className="text-sm text-muted-foreground">Your last 20 parser runs.</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-secondary/50 text-left text-xs uppercase text-muted-foreground">
                <tr>
                  <th className="px-5 py-3">Parser</th>
                  <th className="px-5 py-3">Date</th>
                  <th className="px-5 py-3">Time</th>
                  <th className="px-5 py-3">Status</th>
                </tr>
              </thead>
              <tbody>
                {events.slice(0, 20).map(e => {
                  const d = new Date(e.timestamp);
                  return (
                    <tr key={e.id} className="border-t border-border">
                      <td className="px-5 py-3 font-medium">{e.parser}</td>
                      <td className="px-5 py-3 text-muted-foreground">{d.toLocaleDateString("en-IN")}</td>
                      <td className="px-5 py-3 text-muted-foreground">{d.toLocaleTimeString("en-IN")}</td>
                      <td className="px-5 py-3"><span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700">Success</span></td>
                    </tr>
                  );
                })}
                {events.length === 0 && (
                  <tr><td colSpan={4} className="px-5 py-8 text-center text-muted-foreground">No activity yet. Run a parser above to get started.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
      <Footer />
      <CookieNotice />
    </div>
  );
}

function StatCard({ icon: Icon, label, value }: { icon: any; label: string; value: number }) {
  return (
    <div className="rounded-2xl border border-border bg-card p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm text-muted-foreground">{label}</span>
        <Icon className="h-4 w-4 text-primary" />
      </div>
      <div className="mt-2 font-display text-3xl font-bold">{value.toLocaleString("en-IN")}</div>
    </div>
  );
}
function ChartCard({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <div className="rounded-2xl border border-border bg-card p-5 shadow-sm">
      <h3 className="font-semibold">{title}</h3>
      <p className="mb-4 text-xs text-muted-foreground">{subtitle}</p>
      {children}
    </div>
  );
}
