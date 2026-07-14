import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { signup } from "@/lib/auth";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import { CookieNotice } from "@/components/CookieNotice";

export const Route = createFileRoute("/signup")({
  component: SignupPage,
  head: () => ({ meta: [{ title: "Create account — Reconova" }, { name: "description", content: "Create your Reconova account." }] }),
});

function SignupPage() {
  const nav = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [loading, setLoading] = useState(false);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password.length < 6) return toast.error("Password must be at least 6 characters");
    if (form.password !== form.confirm) return toast.error("Passwords do not match");
    setLoading(true);
    try {
      const u = signup(form.name.trim(), form.email.trim(), form.password);
      toast.success(`Welcome, ${u.name}!`);
      nav({ to: "/dashboard" });
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Sign up failed");
    } finally { setLoading(false); }
  };

  return (
    <div className="grid min-h-screen md:grid-cols-2">
      <div className="hidden bg-gradient-hero md:flex md:flex-col md:justify-between md:p-12">
        <Link to="/" className="flex items-center gap-2">
          <div className="grid h-10 w-10 place-items-center rounded-lg bg-gradient-brand text-white"><Sparkles className="h-5 w-5" /></div>
          <span className="font-display text-2xl font-bold">Reconova</span>
        </Link>
        <div>
          <h2 className="font-display text-4xl font-bold leading-tight">Start your free trial today.</h2>
          <p className="mt-3 max-w-md text-muted-foreground">No credit card. No cookies. Just a single sign-up and you're in.</p>
          <ul className="mt-6 space-y-2 text-sm">
            <li>✓ All parsers included</li>
            <li>✓ Live activity dashboard</li>
            <li>✓ INR-first billing</li>
          </ul>
        </div>
        <p className="text-xs text-muted-foreground">Our site does not store any kind of cookies.</p>
      </div>

      <div className="flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <h1 className="text-3xl font-bold">Create your account</h1>
          <p className="mt-2 text-sm text-muted-foreground">Get started in under a minute.</p>

          <form onSubmit={submit} className="mt-8 space-y-4">
            <div className="space-y-2">
              <Label htmlFor="n">Full name</Label>
              <Input id="n" required value={form.name} onChange={e => setForm({...form, name: e.target.value})} placeholder="Priya Sharma" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="e">Email</Label>
              <Input id="e" type="email" required value={form.email} onChange={e => setForm({...form, email: e.target.value})} placeholder="you@company.in" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="p">Password</Label>
              <Input id="p" type="password" required value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="cp">Confirm password</Label>
              <Input id="cp" type="password" required value={form.confirm} onChange={e => setForm({...form, confirm: e.target.value})} />
            </div>
            <Button type="submit" size="lg" disabled={loading} className="w-full bg-gradient-brand text-white shadow-soft">
              {loading ? "Creating..." : "Create account"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-muted-foreground">
            Already have an account? <Link to="/login" className="font-medium text-primary hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
      <CookieNotice />
    </div>
  );
}
