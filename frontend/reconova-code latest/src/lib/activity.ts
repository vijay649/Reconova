// Tracks parser usage activity for user + admin dashboards.
const KEY = "reconova_activity";

export interface ActivityEvent {
  id: string;
  userId: string;
  userEmail: string;
  parser: string;
  timestamp: string; // ISO
}

export const PARSERS = ["Zomato", "Blinkit", "Amazon", "Flipkart", "Swiggy", "Zepto", "BigBasket"] as const;
export type Parser = typeof PARSERS[number];

function read(): ActivityEvent[] {
  if (typeof window === "undefined") return [];
  try { return JSON.parse(localStorage.getItem(KEY) || "[]"); } catch { return []; }
}
function write(a: ActivityEvent[]) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, JSON.stringify(a));
}

export function seedActivity(users: { id: string; email: string }[]) {
  if (read().length > 0) return;
  const events: ActivityEvent[] = [];
  const now = Date.now();
  for (const u of users) {
    const count = 10 + Math.floor(Math.random() * 25);
    for (let i = 0; i < count; i++) {
      const parser = PARSERS[Math.floor(Math.random() * PARSERS.length)];
      const ts = new Date(now - Math.floor(Math.random() * 30) * 86400000 - Math.floor(Math.random() * 86400000));
      events.push({
        id: "a_" + Math.random().toString(36).slice(2, 10),
        userId: u.id, userEmail: u.email, parser, timestamp: ts.toISOString(),
      });
    }
  }
  write(events);
}

export function logActivity(userId: string, userEmail: string, parser: string) {
  const all = read();
  all.push({
    id: "a_" + Math.random().toString(36).slice(2, 10),
    userId, userEmail, parser, timestamp: new Date().toISOString(),
  });
  write(all);
}

export const listActivity = read;

export function activityByUser(userId: string) {
  return read().filter(e => e.userId === userId).sort((a, b) => b.timestamp.localeCompare(a.timestamp));
}
