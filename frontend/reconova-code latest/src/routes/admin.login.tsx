import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { login, seedIfEmpty, getSession } from "@/lib/auth";
import { toast } from "sonner";
import { ShieldCheck } from "lucide-react";

export const Route = createFileRoute("/admin/login")({
  component: AdminLogin,
  head: () => ({ meta: [{ title: "Admin Login — Reconova" }] }),
});

function AdminLogin() {
  const nav = useNavigate();
  const [email, setEmail] = useState("admin@reconova.in");
  const [password, setPassword] = useState("admin123");

  useEffect(() => {
    seedIfEmpty();
    const s = getSession();
    if (s?.role === "admin") nav({ to: "/admin" });
  }, [nav]);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const u = login(email, password, "admin");
      toast.success(`Welcome, ${u.name}`);
      nav({ to: "/admin" });
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-8 text-slate-100 shadow-2xl">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-lg bg-primary text-white"><ShieldCheck className="h-5 w-5" /></div>
          <div>
            <h1 className="text-xl font-bold">Reconova Admin</h1>
            <p className="text-xs text-slate-400">Restricted area · Authorized personnel only</p>
          </div>
        </div>
        <form onSubmit={submit} className="mt-8 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="e" className="text-slate-300">Admin email</Label>
            <Input id="e" type="email" required value={email} onChange={e => setEmail(e.target.value)} className="border-slate-700 bg-slate-950 text-slate-100" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="p" className="text-slate-300">Password</Label>
            <Input id="p" type="password" required value={password} onChange={e => setPassword(e.target.value)} className="border-slate-700 bg-slate-950 text-slate-100" />
          </div>
          <Button type="submit" size="lg" className="w-full bg-primary text-white hover:bg-primary/90">Sign in to admin</Button>
        </form>
        <div className="mt-6 flex justify-between text-xs text-slate-400">
          <Link to="/forgot-password" className="hover:text-slate-200">Forgot password?</Link>
          <Link to="/login" className="hover:text-slate-200">User login →</Link>
        </div>
      </div>
    </div>
  );
}
