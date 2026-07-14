import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CookieNotice } from "@/components/CookieNotice";
import { Button } from "@/components/ui/button";
import { Check, IndianRupee } from "lucide-react";
import { toast } from "sonner";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { getSession } from "@/lib/auth";

export const Route = createFileRoute("/subscription")({
  component: Subscription,
  head: () => ({ meta: [{ title: "Pricing & Subscription — Reconova" }, { name: "description", content: "Simple INR pricing. Pay via Razorpay." }] }),
});

const PLANS = [
  { name: "Starter", price: 499, tag: "For individuals", features: ["3 parsers", "1,000 runs / month", "Email support", "Basic analytics"] },
  { name: "Pro", price: 1999, tag: "Most popular", features: ["All parsers", "20,000 runs / month", "Priority support", "Advanced analytics", "API access"], featured: true },
  { name: "Enterprise", price: 7999, tag: "For teams", features: ["Unlimited runs", "SLA + dedicated support", "SSO & role management", "Custom integrations"] },
];

function Subscription() {
  const nav = useNavigate();
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<typeof PLANS[number] | null>(null);
  const [processing, setProcessing] = useState(false);

  const startCheckout = (plan: typeof PLANS[number]) => {
    const s = getSession();
    if (!s) { toast.error("Please sign in first"); nav({ to: "/login" }); return; }
    setSelected(plan);
    setOpen(true);
  };

  const pay = () => {
    setProcessing(true);
    // Mock Razorpay flow. In prod: window.Razorpay checkout with orderId from FastAPI.
    setTimeout(() => {
      setProcessing(false);
      setOpen(false);
      toast.success(`Payment successful! ${selected?.name} plan activated.`);
    }, 1600);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <section className="bg-gradient-hero">
          <div className="mx-auto max-w-4xl px-6 py-16 text-center">
            <h1 className="text-4xl font-bold md:text-5xl">Simple, transparent pricing</h1>
            <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">All prices in Indian Rupees (₹). Pay securely via Razorpay — UPI, cards, netbanking & wallets supported.</p>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-6 py-16">
          <div className="grid gap-6 md:grid-cols-3">
            {PLANS.map(p => (
              <div key={p.name} className={`relative rounded-2xl border p-6 shadow-sm transition hover:shadow-soft ${p.featured ? "border-primary bg-card ring-2 ring-primary/30" : "border-border bg-card"}`}>
                {p.featured && <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-gradient-brand px-3 py-1 text-xs font-semibold text-white shadow-soft">Most popular</span>}
                <p className="text-sm font-medium text-primary">{p.tag}</p>
                <h3 className="mt-1 text-2xl font-bold">{p.name}</h3>
                <div className="mt-4 flex items-end gap-1">
                  <IndianRupee className="mb-1.5 h-5 w-5 text-muted-foreground" />
                  <span className="font-display text-5xl font-extrabold">{p.price.toLocaleString("en-IN")}</span>
                  <span className="mb-2 text-sm text-muted-foreground">/month</span>
                </div>
                <ul className="mt-6 space-y-3 text-sm">
                  {p.features.map(f => (
                    <li key={f} className="flex items-start gap-2"><Check className="mt-0.5 h-4 w-4 text-emerald-600" /> {f}</li>
                  ))}
                </ul>
                <Button className={`mt-8 w-full ${p.featured ? "bg-gradient-brand text-white shadow-soft" : ""}`} variant={p.featured ? "default" : "outline"} onClick={() => startCheckout(p)}>
                  Subscribe — ₹{p.price.toLocaleString("en-IN")}/mo
                </Button>
              </div>
            ))}
          </div>

          <p className="mt-8 text-center text-xs text-muted-foreground">
            All plans include GST. Cancel anytime. Amounts shown in INR.
          </p>
        </section>
      </main>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Complete your purchase</DialogTitle>
            <DialogDescription>
              You're subscribing to <strong>{selected?.name}</strong> at <strong>₹{selected?.price.toLocaleString("en-IN")}/month</strong>. This is a demo Razorpay checkout — no real payment is made.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3 py-2">
            <div className="space-y-1.5"><Label>Card number</Label><Input placeholder="4242 4242 4242 4242" /></div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5"><Label>Expiry</Label><Input placeholder="MM/YY" /></div>
              <div className="space-y-1.5"><Label>CVV</Label><Input placeholder="123" /></div>
            </div>
            <div className="space-y-1.5"><Label>Name on card</Label><Input placeholder="Priya Sharma" /></div>
          </div>
          <Button size="lg" className="w-full bg-gradient-brand text-white" onClick={pay} disabled={processing}>
            {processing ? "Processing..." : `Pay ₹${selected?.price.toLocaleString("en-IN")}`}
          </Button>
          <p className="text-center text-xs text-muted-foreground">Powered by Razorpay · 100% Indian Rupees</p>
        </DialogContent>
      </Dialog>
      <Footer />
      <CookieNotice />
    </div>
  );
}
