import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useEffect, useMemo, useState } from "react";
import { getSession, listUsers, deleteUser, seedIfEmpty, logout, type User } from "@/lib/auth";
import { PARSERS, listActivity, seedActivity } from "@/lib/activity";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Bar, BarChart, CartesianGrid, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { CookieNotice } from "@/components/CookieNotice";
import { Activity, LogOut, ShieldCheck, Trash2, Users } from "lucide-react";

export const Route = createFileRoute("/admin")({
  component: AdminDashboard,
  head: () => ({ meta: [{ title: "Admin Dashboard — Reconova" }] }),
});

const COLORS = ["#2563EB", "#0891B2", "#059669", "#D97706", "#DC2626", "#7C3AED", "#DB2777"];

function AdminDashboard() {
  const nav = useNavigate();
  const [session, setSession] = useState<ReturnType<typeof getSession>>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [confirmId, setConfirmId] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    seedIfEmpty();
    const s = getSession();
    if (!s) { nav({ to: "/admin/login" }); return; }
    if (s.role !== "admin") { nav({ to: "/dashboard" }); return; }
    seedActivity(listUsers().map(u => ({ id: u.id, email: u.email })));
    setSession(s);
    setUsers(listUsers());
  }, [nav, tick]);

  const events = useMemo(() => listActivity(), [tick, users]);

  const parserData = useMemo(() => {
    const m = new Map<string, number>();
    PARSERS.forEach(p => m.set(p, 0));
    events.forEach(e => m.set(e.parser, (m.get(e.parser) || 0) + 1));
    return Array.from(m, ([name, count]) => ({ name, count }));
  }, [events]);

  const dailyData = useMemo(() => {
    const days: Record<string, number> = {};
    for (let i = 13; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      days[d.toISOString().slice(0, 10)] = 0;
    }
    events.forEach(e => {
      const k = e.timestamp.slice(0, 10);
      if (k in days) days[k]++;
    });
    return Object.entries(days).map(([date, count]) => ({ date: date.slice(5), count }));
  }, [events]);

  const userLeaderboard = useMemo(() => {
    const m = new Map<string, { email: string; count: number }>();
    events.forEach(e => {
      const cur = m.get(e.userId) || { email: e.userEmail, count: 0 };
      cur.count += 1;
      m.set(e.userId, cur);
    });
    return Array.from(m, ([userId, v]) => ({ userId, ...v })).sort((a, b) => b.count - a.count);
  }, [events]);

  const remove = (id: string) => {
    if (id === session?.id) return toast.error("You can't delete your own account");
    deleteUser(id);
    setConfirmId(null);
    setTick(t => t + 1);
    toast.success("User deleted");
  };

  const doLogout = () => {
    logout();
    setSession(null);
    if (typeof window !== "undefined") {
      window.location.href = "/admin/login";
    } else {
      nav({ to: "/admin/login", replace: true });
    }
  };

  if (!session) return null;

  const totalRuns = events.length;
  const totalUsers = users.length;
  const activeUsers = new Set(events.map(e => e.userId)).size;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Top bar */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-gradient-brand text-white"><ShieldCheck className="h-5 w-5" /></div>
            <div>
              <h1 className="font-display text-lg font-bold">Reconova · Admin</h1>
              <p className="text-xs text-slate-400">Signed in as {session.email}</p>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={doLogout} className="border-slate-700 bg-transparent text-slate-100 hover:bg-slate-800"><LogOut className="mr-1 h-4 w-4" /> Sign out</Button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-10">
        {/* Stats */}
        <div className="grid gap-4 md:grid-cols-4">
          <AdminStat icon={Users} label="Total users" value={totalUsers} accent="from-blue-500 to-cyan-500" />
          <AdminStat icon={Activity} label="Total parser runs" value={totalRuns} accent="from-emerald-500 to-teal-500" />
          <AdminStat icon={Users} label="Active users" value={activeUsers} accent="from-orange-500 to-rose-500" />
          <AdminStat icon={ShieldCheck} label="Available parsers" value={PARSERS.length} accent="from-violet-500 to-fuchsia-500" />
        </div>

        {/* Charts */}
        <div className="mt-8 grid gap-6 lg:grid-cols-3">
          <AdminChart title="Runs by parser" className="lg:col-span-2">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={parserData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" fontSize={12} stroke="#94a3b8" />
                <YAxis fontSize={12} stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, color: "#f8fafc" }} />
                <Bar dataKey="count" radius={[8,8,0,0]}>
                  {parserData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </AdminChart>

          <AdminChart title="Parser distribution">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={parserData.filter(d => d.count > 0)} dataKey="count" nameKey="name" outerRadius={100} innerRadius={55}>
                  {parserData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, color: "#f8fafc" }} />
                <Legend wrapperStyle={{ fontSize: 11, color: "#cbd5e1" }} />
              </PieChart>
            </ResponsiveContainer>
          </AdminChart>
        </div>

        <div className="mt-6">
          <AdminChart title="Platform activity (last 14 days)">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={dailyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" fontSize={12} stroke="#94a3b8" />
                <YAxis fontSize={12} stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 8, color: "#f8fafc" }} />
                <Line type="monotone" dataKey="count" stroke="#2563EB" strokeWidth={3} dot={{ r: 4, fill: "#2563EB" }} />
              </LineChart>
            </ResponsiveContainer>
          </AdminChart>
        </div>

        {/* Users table */}
        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900">
          <div className="border-b border-slate-800 p-5">
            <h2 className="text-lg font-semibold">Users</h2>
            <p className="text-sm text-slate-400">Manage all Reconova accounts.</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-950/50 text-left text-xs uppercase text-slate-400">
                <tr>
                  <th className="px-5 py-3">Name</th>
                  <th className="px-5 py-3">Email</th>
                  <th className="px-5 py-3">Role</th>
                  <th className="px-5 py-3">Plan</th>
                  <th className="px-5 py-3">Runs</th>
                  <th className="px-5 py-3">Joined</th>
                  <th className="px-5 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(u => {
                  const runs = userLeaderboard.find(x => x.userId === u.id)?.count || 0;
                  return (
                    <tr key={u.id} className="border-t border-slate-800">
                      <td className="px-5 py-3 font-medium">{u.name}</td>
                      <td className="px-5 py-3 text-slate-400">{u.email}</td>
                      <td className="px-5 py-3">
                        <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${u.role === "admin" ? "bg-primary/20 text-primary" : "bg-slate-800 text-slate-300"}`}>{u.role}</span>
                      </td>
                      <td className="px-5 py-3 text-slate-300">{u.plan || "Free"}</td>
                      <td className="px-5 py-3 text-slate-300">{runs}</td>
                      <td className="px-5 py-3 text-slate-400">{new Date(u.createdAt).toLocaleDateString("en-IN")}</td>
                      <td className="px-5 py-3 text-right">
                        <Button size="sm" variant="outline" className="border-red-500/40 bg-transparent text-red-400 hover:bg-red-500/10" disabled={u.id === session.id} onClick={() => setConfirmId(u.id)}>
                          <Trash2 className="mr-1 h-3.5 w-3.5" /> Delete
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent activity across platform */}
        <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900">
          <div className="border-b border-slate-800 p-5">
            <h2 className="text-lg font-semibold">Recent platform activity</h2>
            <p className="text-sm text-slate-400">Who used which parser and when.</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-950/50 text-left text-xs uppercase text-slate-400">
                <tr>
                  <th className="px-5 py-3">User</th>
                  <th className="px-5 py-3">Parser</th>
                  <th className="px-5 py-3">Date</th>
                  <th className="px-5 py-3">Time</th>
                </tr>
              </thead>
              <tbody>
                {[...events].sort((a,b) => b.timestamp.localeCompare(a.timestamp)).slice(0, 25).map(e => {
                  const d = new Date(e.timestamp);
                  return (
                    <tr key={e.id} className="border-t border-slate-800">
                      <td className="px-5 py-3">{e.userEmail}</td>
                      <td className="px-5 py-3 font-medium">{e.parser}</td>
                      <td className="px-5 py-3 text-slate-400">{d.toLocaleDateString("en-IN")}</td>
                      <td className="px-5 py-3 text-slate-400">{d.toLocaleTimeString("en-IN")}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <AlertDialog open={!!confirmId} onOpenChange={(o) => !o && setConfirmId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this user?</AlertDialogTitle>
            <AlertDialogDescription>This will remove the account permanently. This action cannot be undone.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={() => confirmId && remove(confirmId)} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">Delete</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      <CookieNotice />
    </div>
  );
}

function AdminStat({ icon: Icon, label, value, accent }: { icon: any; label: string; value: number; accent: string }) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <div className={`absolute -right-6 -top-6 h-24 w-24 rounded-full bg-gradient-to-br ${accent} opacity-20 blur-2xl`} />
      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-400">{label}</span>
        <Icon className="h-4 w-4 text-slate-300" />
      </div>
      <div className="mt-2 font-display text-3xl font-bold text-white">{value.toLocaleString("en-IN")}</div>
    </div>
  );
}

function AdminChart({ title, children, className = "" }: { title: string; children: React.ReactNode; className?: string }) {
  return (
    <div className={`rounded-2xl border border-slate-800 bg-slate-900 p-5 ${className}`}>
      <h3 className="mb-4 font-semibold">{title}</h3>
      {children}
    </div>
  );
}
