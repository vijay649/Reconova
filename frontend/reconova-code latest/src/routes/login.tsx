import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { login, seedIfEmpty, getSession } from "@/lib/auth";
import { toast } from "sonner";
import { CookieNotice } from "@/components/CookieNotice";
import { Sparkles, ArrowRight } from "lucide-react";

export const Route = createFileRoute("/login")({
  component: LoginPage,
  head: () => ({ meta: [{ title: "Login — Reconova" }, { name: "description", content: "Sign in to your Reconova account." }] }),
});

function LoginPage() {
  const nav = useNavigate();
  const [email, setEmail] = useState("demo@reconova.in");
  const [password, setPassword] = useState("demo123");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    seedIfEmpty();
    const s = getSession();
    if (s) nav({ to: s.role === "admin" ? "/admin" : "/dashboard" });
  }, [nav]);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const u = login(email, password);
      toast.success(`Welcome back, ${u.name}!`);
      nav({ to: u.role === "admin" ? "/admin" : "/dashboard" });
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
      }
  };

  return (
    <div className="grid min-h-screen md:grid-cols-2">
      <div className="hidden bg-gradient-hero md:flex md:flex-col md:justify-between md:p-12">
        <Link to="/" className="flex items-center gap-2">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-gradient-brand text-white"><Sparkles className="h-5 w-5" /></div>
          <span className="font-display text-2xl font-bold">Reconova</span>
        </Link>
        <div>
          <h2 className="font-display text-4xl font-bold leading-tight">Reconcile smarter.<br/>Ship faster.</h2>
          <p className="mt-3 max-w-md text-muted-foreground">One login. Every parser you run — Zomato, Blinkit, Amazon, Flipkart, Swiggy — in a single dashboard.</p>
        </div>
        <p className="text-xs text-muted-foreground">Our site does not store any kind of cookies.</p>
      </div>

      <div className="flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <div className="md:hidden mb-8 flex items-center gap-2">
            <div className="grid h-10 w-10 place-items-center rounded-lg bg-gradient-brand text-white"><Sparkles className="h-5 w-5" /></div>
            <span className="font-display text-2xl font-bold">Reconova</span>
          </div>
          <h1 className="text-3xl font-bold">Welcome back</h1>
          <p className="mt-2 text-sm text-muted-foreground">Sign in to your Reconova account.</p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" required value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="pwd">Password</Label>
                <Link to="/forgot-password" className="text-xs text-primary hover:underline">Forgot?</Link>
              </div>
              <Input id="pwd" type="password" required value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <Button type="submit" size="lg" disabled={loading} className="w-full bg-gradient-brand text-white shadow-soft">
              {loading ? "Signing in..." : <>Sign in <ArrowRight className="ml-1 h-4 w-4" /></>}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            New here? <Link to="/signup" className="font-medium text-primary hover:underline">Create an account</Link>
          </p>
        </div>
      </div>
      <CookieNotice />
    </div>
  );
}
