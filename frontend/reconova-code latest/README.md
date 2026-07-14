# Reconova — Frontend

Modern React + TanStack Start + Tailwind v4 frontend for **Reconova**, a unified parser dashboard for Indian marketplaces (Zomato, Blinkit, Amazon, Flipkart, Swiggy, Zepto, BigBasket).

## Features

- Landing page, Products, INR Subscription (₹) with Razorpay-style checkout dialog
- Login / Signup / Forgot password / Reset password
- **User Dashboard** — parser cards, run parsers, activity log, bar + line charts
- **Admin Dashboard** — user table with delete, platform-wide activity, bar/pie/line charts
- Separate `/admin/login` for admin access
- Responsive navbar with Home / Products / Subscription
- Footer with contact info
- "Our site does not store any kind of cookies" notice
- Mock auth stored in `localStorage` — swap out with your FastAPI backend

## Run locally

```bash
bun install     # or: npm install
bun run dev     # or: npm run dev
```

Preview at http://localhost:8080

Demo accounts (auto-seeded on first visit):
- **User**: `demo@reconova.in` / `demo123`
- **Admin**: `admin@reconova.in` / `admin123` (log in at `/admin/login`)

## Connecting to FastAPI

1. Create `.env` in project root:
   ```
   VITE_API_URL=http://localhost:8000
   ```
2. Use the helper in `src/lib/api.ts`:
   ```ts
   import { apiRequest } from "@/lib/api";
   const user = await apiRequest<{ token: string }>("/auth/login", {
     method: "POST",
     body: JSON.stringify({ email, password }),
   });
   ```
3. Replace calls inside `src/lib/auth.ts` (`login`, `signup`, `resetPassword`, `listUsers`, `deleteUser`) and `src/lib/activity.ts` (`logActivity`, `listActivity`, `activityByUser`) with real API calls.
4. For Razorpay, in `src/routes/subscription.tsx` replace the mock `pay()` with:
   ```ts
   const { orderId } = await apiRequest("/payments/create-order", { method: "POST", body: JSON.stringify({ planId: selected.name, amount: selected.price * 100 }) });
   const rzp = new (window as any).Razorpay({ key: "rzp_test_xxx", order_id: orderId, currency: "INR", ... });
   rzp.open();
   ```
   And add `<script src="https://checkout.razorpay.com/v1/checkout.js">` to `src/routes/__root.tsx` head.

## Tech stack

- React 19 + TypeScript
- TanStack Start (file-based routing, SSR-capable)
- Tailwind CSS v4
- shadcn/ui (Radix primitives)
- Recharts (charts)
- Sonner (toasts)
- Lucide icons
