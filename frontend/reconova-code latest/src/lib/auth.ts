// Simple mock auth stored in localStorage. Replace with FastAPI later.
export type Role = "user" | "admin";
export interface User {
  id: string;
  name: string;
  email: string;
  password: string; // mock only
  role: Role;
  createdAt: string;
  plan?: "Free" | "Starter" | "Pro" | "Enterprise";
}

const USERS_KEY = "reconova_users";
const SESSION_KEY = "reconova_session";

function read<T>(k: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try { return JSON.parse(localStorage.getItem(k) || "null") ?? fallback; } catch { return fallback; }
}
function write(k: string, v: unknown) {
  if (typeof window === "undefined") return;
  localStorage.setItem(k, JSON.stringify(v));
}

export function seedIfEmpty() {
  const users = read<User[]>(USERS_KEY, []);
  if (users.length === 0) {
    const seed: User[] = [
      { id: "u_admin", name: "Admin", email: "admin@reconova.in", password: "admin123", role: "admin", createdAt: new Date().toISOString(), plan: "Enterprise" },
      { id: "u_demo", name: "Demo User", email: "demo@reconova.in", password: "demo123", role: "user", createdAt: new Date().toISOString(), plan: "Starter" },
    ];
    write(USERS_KEY, seed);
  }
}

export const listUsers = () => read<User[]>(USERS_KEY, []);
export const saveUsers = (u: User[]) => write(USERS_KEY, u);

export function signup(name: string, email: string, password: string, role: Role = "user"): User {
  const users = listUsers();
  if (users.find(u => u.email.toLowerCase() === email.toLowerCase())) {
    throw new Error("Email already registered");
  }
  const user: User = { id: "u_" + Math.random().toString(36).slice(2, 9), name, email, password, role, createdAt: new Date().toISOString(), plan: "Free" };
  users.push(user);
  saveUsers(users);
  setSession(user);
  return user;
}

export function login(email: string, password: string, role?: Role): User {
  const users = listUsers();
  const u = users.find(x => x.email.toLowerCase() === email.toLowerCase() && x.password === password);
  if (!u) throw new Error("Invalid credentials");
  if (role && u.role !== role) throw new Error(`This account is not a ${role} account`);
  setSession(u);
  return u;
}

export function resetPassword(email: string, newPassword: string) {
  const users = listUsers();
  const idx = users.findIndex(u => u.email.toLowerCase() === email.toLowerCase());
  if (idx === -1) throw new Error("Email not found");
  users[idx].password = newPassword;
  saveUsers(users);
}

export function logout() {
  if (typeof window !== "undefined") localStorage.removeItem(SESSION_KEY);
}

export function setSession(u: User) { write(SESSION_KEY, { id: u.id, role: u.role, email: u.email, name: u.name }); }
export function getSession(): { id: string; role: Role; email: string; name: string } | null {
  return read(SESSION_KEY, null as any);
}

export function deleteUser(id: string) {
  saveUsers(listUsers().filter(u => u.id !== id));
}
