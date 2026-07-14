import { createFileRoute, Link, useNavigate, useSearch } from "@tanstack/react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { resetPassword } from "@/lib/auth";

export const Route = createFileRoute("/reset-password")({
  component: ResetPage,
  validateSearch: (s: Record<string, unknown>) => ({ email: (s.email as string) || "" }),
  head: () => ({ meta: [{ title: "Reset password — Reconova" }] }),
});

function ResetPage() {
  const nav = useNavigate();
  const { email: initialEmail } = useSearch({ from: "/reset-password" });
  const [email, setEmail] = useState(initialEmail);
  const [pwd, setPwd] = useState("");
  const [confirm, setConfirm] = useState("");

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (pwd.length < 6) return toast.error("Password must be at least 6 characters");
    if (pwd !== confirm) return toast.error("Passwords do not match");
    try {
      resetPassword(email, pwd);
      toast.success("Password updated. Please sign in.");
      nav({ to: "/login" });
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Reset failed");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-hero px-6">
      <div className="w-full max-w-md rounded-2xl border border-border bg-card p-8 shadow-soft">
        <h1 className="text-2xl font-bold">Set a new password</h1>
        <form onSubmit={submit} className="mt-6 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="e">Email</Label>
            <Input id="e" type="email" required value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="p">New password</Label>
            <Input id="p" type="password" required value={pwd} onChange={e => setPwd(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cp">Confirm new password</Label>
            <Input id="cp" type="password" required value={confirm} onChange={e => setConfirm(e.target.value)} />
          </div>
          <Button type="submit" size="lg" className="w-full bg-gradient-brand text-white">Update password</Button>
        </form>
        <p className="mt-4 text-center text-sm text-muted-foreground">
          <Link to="/login" className="text-primary hover:underline">Back to login</Link>
        </p>
      </div>
    </div>
  );
}
