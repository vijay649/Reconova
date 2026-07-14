import { createFileRoute, Link } from "@tanstack/react-router";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CookieNotice } from "@/components/CookieNotice";
import { PARSERS } from "@/lib/activity";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

export const Route = createFileRoute("/products")({
  component: Products,
  head: () => ({ meta: [{ title: "Products — Reconova" }, { name: "description", content: "All parsers offered by Reconova." }] }),
});

const COLORS = ["#2563EB", "#0891B2", "#059669", "#D97706", "#DC2626", "#7C3AED", "#DB2777"];

function Products() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <section className="bg-gradient-hero">
          <div className="mx-auto max-w-7xl px-6 py-16 text-center">
            <h1 className="text-4xl font-bold md:text-5xl">All parsers, one platform</h1>
            <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">Battle-tested parsers for India's biggest marketplaces. Plug them in, and get reconciled data instantly.</p>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-16">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {PARSERS.map((p, i) => (
              <div key={p} className="group rounded-2xl border border-border bg-card p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-soft">
                <div className="grid h-12 w-12 place-items-center rounded-xl text-lg font-bold text-white" style={{ background: COLORS[i % COLORS.length] }}>{p[0]}</div>
                <h3 className="mt-5 text-xl font-semibold">{p} Parser</h3>
                <p className="mt-1 text-sm text-muted-foreground">Extract, normalize and reconcile orders, payouts, refunds & fees for {p}.</p>
                <ul className="mt-4 space-y-2 text-sm">
                  <li className="flex items-center gap-2"><Check className="h-4 w-4 text-emerald-600" /> Auto-schema mapping</li>
                  <li className="flex items-center gap-2"><Check className="h-4 w-4 text-emerald-600" /> INR-first reporting</li>
                  <li className="flex items-center gap-2"><Check className="h-4 w-4 text-emerald-600" /> FastAPI-ready endpoints</li>
                </ul>
                <Link to="/parser/$name" params={{ name: p }}><Button className="mt-5 w-full bg-gradient-brand text-white">Open {p} parser</Button></Link>
              </div>
            ))}
          </div>
        </section>
      </main>
      <Footer />
      <CookieNotice />
    </div>
  );
}
