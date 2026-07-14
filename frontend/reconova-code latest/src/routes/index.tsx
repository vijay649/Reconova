import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CookieNotice } from "@/components/CookieNotice";
import { Button } from "@/components/ui/button";
import { getSession, seedIfEmpty, listUsers } from "@/lib/auth";
import { seedActivity } from "@/lib/activity";
import { ArrowRight, BarChart3, Boxes, ShieldCheck, Zap } from "lucide-react";

export const Route = createFileRoute("/")({
  component: Landing,
  head: () => ({
    meta: [
      { title: "Reconova — Unified Parser Dashboard for Indian Marketplaces" },
      { name: "description", content: "Track Zomato, Blinkit, Amazon, Flipkart & Swiggy parsers in one dashboard. Built for India, priced in INR." },
    ],
  }),
});

function Landing() {
  const nav = useNavigate();
  useEffect(() => {
    seedIfEmpty();
    seedActivity(listUsers().map(u => ({ id: u.id, email: u.email })));
    // Requirement: on start, take user to login/signup if not logged in.
    const s = getSession();
    if (!s) nav({ to: "/login" });
  }, [nav]);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <section className="relative overflow-hidden bg-gradient-hero">
          <div className="mx-auto grid max-w-7xl gap-12 px-6 py-20 md:grid-cols-2 md:py-28">
            <div className="flex flex-col justify-center">
              <span className="inline-flex w-fit items-center gap-2 rounded-full border border-primary/20 bg-white px-3 py-1 text-xs font-medium text-primary shadow-sm">
                <Zap className="h-3.5 w-3.5" /> Built for Indian marketplaces
              </span>
              <h1 className="mt-5 text-4xl font-extrabold leading-tight md:text-6xl">
                One dashboard for <span className="bg-gradient-brand bg-clip-text text-transparent">every parser</span> you run.
              </h1>
              <p className="mt-5 max-w-lg text-lg text-muted-foreground">
                Reconova connects your Zomato, Blinkit, Amazon, Flipkart & Swiggy parsers — so you spend less time switching tools and more time shipping insights.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link to="/signup"><Button size="lg" className="bg-gradient-brand text-white shadow-soft">Create account <ArrowRight className="ml-1 h-4 w-4" /></Button></Link>
                <Link to="/products"><Button size="lg" variant="outline">Explore parsers</Button></Link>
              </div>
              <p className="mt-4 text-xs text-muted-foreground">No credit card required · Pricing in ₹ INR</p>
            </div>
            <div className="relative">
              <div className="absolute -inset-6 rounded-3xl bg-gradient-brand opacity-10 blur-2xl" />
              <div className="relative rounded-2xl border border-border bg-card p-6 shadow-soft">
                <div className="flex items-center justify-between border-b border-border pb-3">
                  <div className="flex items-center gap-2"><div className="h-2.5 w-2.5 rounded-full bg-destructive" /><div className="h-2.5 w-2.5 rounded-full bg-yellow-400" /><div className="h-2.5 w-2.5 rounded-full bg-emerald-500" /></div>
                  <span className="text-xs text-muted-foreground">reconova.in/dashboard</span>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-3">
                  {["Zomato","Blinkit","Amazon","Flipkart"].map((p, i) => (
                    <div key={p} className="rounded-xl border border-border bg-secondary/40 p-4">
                      <div className="text-xs text-muted-foreground">{p} parser</div>
                      <div className="mt-1 font-display text-2xl font-bold">{(120 + i*37).toLocaleString("en-IN")}</div>
                      <div className="mt-2 h-1.5 rounded-full bg-muted"><div className="h-full rounded-full bg-gradient-brand" style={{ width: `${40 + i*15}%` }} /></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-20">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-bold md:text-4xl">Everything you need to reconcile at scale</h2>
            <p className="mt-3 text-muted-foreground">Powerful parsers, transparent activity, and admin controls that just work.</p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {[
              { icon: Boxes, title: "Multi-parser support", desc: "Zomato, Blinkit, Amazon, Flipkart, Swiggy and more — all in one place." },
              { icon: BarChart3, title: "Activity insights", desc: "See which parser is used, how often, and by whom, with beautiful charts." },
              { icon: ShieldCheck, title: "Privacy first", desc: "Our site does not store any kind of cookies. Your data stays yours." },
            ].map(f => (
              <div key={f.title} className="rounded-2xl border border-border bg-card p-6 shadow-sm transition hover:shadow-soft">
                <div className="grid h-11 w-11 place-items-center rounded-lg bg-accent text-primary"><f.icon className="h-5 w-5" /></div>
                <h3 className="mt-4 text-lg font-semibold">{f.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{f.desc}</p>
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
