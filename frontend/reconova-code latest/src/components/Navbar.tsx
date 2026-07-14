import { Link, useNavigate, useRouterState } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { getSession, logout } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { LogOut, Menu, X, Sparkles } from "lucide-react";

export function Navbar() {
  const nav = useNavigate();
  const pathname = useRouterState({ select: s => s.location.pathname });
  const [session, setSession] = useState<ReturnType<typeof getSession>>(null);
  const [open, setOpen] = useState(false);

  useEffect(() => { setSession(getSession()); }, [pathname]);

  const links = [
    { to: "/", label: "Home" },
    { to: "/products", label: "Products" },
    { to: "/subscription", label: "Subscription" },
  ];

  const doLogout = () => { logout(); setSession(null); nav({ to: "/login" }); };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/70 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link to="/" className="flex items-center gap-2">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-brand text-white shadow-soft">
            <Sparkles className="h-5 w-5" />
          </div>
          <span className="font-display text-xl font-bold tracking-tight">Reconova</span>
        </Link>

        <nav className="hidden items-center gap-1 md:flex">
          {links.map(l => (
            <Link
              key={l.to}
              to={l.to}
              className="rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
              activeProps={{ className: "rounded-md px-3 py-2 text-sm font-semibold text-primary bg-accent" }}
              activeOptions={{ exact: true }}
            >
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-2 md:flex">
          {session ? (
            <>
              <Link to={session.role === "admin" ? "/admin" : "/dashboard"}>
                <Button variant="ghost" size="sm">Dashboard</Button>
              </Link>
              <Button size="sm" variant="outline" onClick={doLogout}>
                <LogOut className="mr-1 h-4 w-4" /> Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login"><Button variant="ghost" size="sm">Login</Button></Link>
              <Link to="/signup"><Button size="sm" className="bg-gradient-brand text-white shadow-soft">Get Started</Button></Link>
            </>
          )}
        </div>

        <button className="md:hidden" onClick={() => setOpen(o => !o)} aria-label="Menu">
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="border-t border-border bg-background md:hidden">
          <div className="mx-auto flex max-w-7xl flex-col gap-1 px-4 py-3">
            {links.map(l => (
              <Link key={l.to} to={l.to} onClick={() => setOpen(false)} className="rounded-md px-3 py-2 text-sm font-medium hover:bg-accent">
                {l.label}
              </Link>
            ))}
            {session ? (
              <>
                <Link to={session.role === "admin" ? "/admin" : "/dashboard"} onClick={() => setOpen(false)} className="rounded-md px-3 py-2 text-sm font-medium hover:bg-accent">Dashboard</Link>
                <button onClick={doLogout} className="rounded-md px-3 py-2 text-left text-sm font-medium hover:bg-accent">Logout</button>
              </>
            ) : (
              <>
                <Link to="/login" onClick={() => setOpen(false)} className="rounded-md px-3 py-2 text-sm font-medium hover:bg-accent">Login</Link>
                <Link to="/signup" onClick={() => setOpen(false)} className="rounded-md px-3 py-2 text-sm font-medium hover:bg-accent">Sign up</Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
