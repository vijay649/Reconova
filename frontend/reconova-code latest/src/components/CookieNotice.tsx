import { useEffect, useState } from "react";
import { X, ShieldCheck } from "lucide-react";

const KEY = "reconova_cookie_ack";

export function CookieNotice() {
  const [show, setShow] = useState(false);
  useEffect(() => {
    if (typeof window !== "undefined" && !localStorage.getItem(KEY)) setShow(true);
  }, []);
  if (!show) return null;
  return (
    <div className="fixed inset-x-3 bottom-3 z-50 mx-auto max-w-3xl rounded-xl border border-border bg-card p-4 shadow-soft md:inset-x-auto md:right-6">
      <div className="flex items-start gap-3">
        <ShieldCheck className="mt-0.5 h-5 w-5 text-primary" />
        <div className="flex-1 text-sm">
          <p className="font-semibold">Privacy first</p>
          <p className="text-muted-foreground">
            Our site does <strong>not</strong> store any kind of cookies. Your session stays only on your device.
          </p>
        </div>
        <button onClick={() => { localStorage.setItem(KEY, "1"); setShow(false); }} aria-label="Dismiss" className="rounded-md p-1 hover:bg-accent">
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
