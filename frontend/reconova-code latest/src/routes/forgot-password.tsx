import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { listUsers } from "@/lib/auth";

export const Route = createFileRoute("/forgot-password")({
  component: ForgotPage,
  head: () => ({ meta: [{ title: "Forgot password — Reconova" }] }),
});

function ForgotPage() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const exists = listUsers().find(u => u.email.toLowerCase() === email.toLowerCase());
    if (!exists) return toast.error("No account with that email");
    toast.success("Reset link generated (demo). Redirecting to reset...");
    setTimeout(() => nav({ to: "/reset-password", search: { email } as any }), 900);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-hero px-6">
      <div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-soft">
        <h1 className="text-2xl font-bold">Forgot your password?</h1>
        <p className="mt-2 text-sm text-muted-foreground">Enter your email and we'll send you a reset link.</p>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="e">Email</Label>
            <Input id="e" type="email" required value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <Button type="submit" size="lg" className="w-full bg-gradient-brand text-white">Send reset link</Button>
        </form>
        <p className="mt-4 text-center text-sm text-muted-foreground">
          Remember it? <Link to="/login" className="text-primary hover:underline">Back to login</Link>
        </p>
      </div>
    </div>
  );
}
