// import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
// import { useEffect, useRef, useState } from "react";
// import * as XLSX from "xlsx";
// import { Navbar } from "@/components/Navbar";
// import { Footer } from "@/components/Footer";
// import { CookieNotice } from "@/components/CookieNotice";
// import { Button } from "@/components/ui/button";
// import { getSession } from "@/lib/auth";
// import { logActivity, PARSERS } from "@/lib/activity";
// import { toast } from "sonner";
// import { ArrowLeft, FolderOpen, FileSpreadsheet, Loader2, CheckCircle2, X, Download } from "lucide-react";

// export const Route = createFileRoute("/parser/$name")({
//   component: ParserPage,
//   head: ({ params }) => ({
//     meta: [{ title: `${params.name} Parser — Reconova` }],
//   }),
// });

// interface PickedFile { name: string; path: string; size: number; file: File; }

// function ParserPage() {
//   const { name } = Route.useParams();
//   const nav = useNavigate();
//   const inputRef = useRef<HTMLInputElement | null>(null);
//   const [session, setSession] = useState<ReturnType<typeof getSession>>(null);
//   const [files, setFiles] = useState<PickedFile[]>([]);
//   const [folderName, setFolderName] = useState<string>("");
//   const [processing, setProcessing] = useState(false);
//   const [done, setDone] = useState(false);
//   const [blobUrl, setBlobUrl] = useState<string | null>(null);

//   const isValid = PARSERS.includes(name as (typeof PARSERS)[number]);

//   useEffect(() => {
//     const s = getSession();
//     if (!s) { nav({ to: "/login" }); return; }
//     setSession(s);
//   }, [nav]);

//   const onPick = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const list = e.target.files;
//     if (!list || list.length === 0) return;
//     const arr: PickedFile[] = [];
//     let root = "";
//     for (let i = 0; i < list.length; i++) {
//       const f = list[i];
//       const rel: string = (f as File & { webkitRelativePath?: string }).webkitRelativePath || f.name;
//       if (!root && rel.includes("/")) root = rel.split("/")[0];
//       arr.push({ name: f.name, path: rel, size: f.size, file: f });
//     }
//     setFolderName(root || "Selected files");
//     setFiles(arr);
//     setDone(false);
//     if (blobUrl) { URL.revokeObjectURL(blobUrl); setBlobUrl(null); }
//   };

//   const reset = () => {
//     setFiles([]); setFolderName(""); setDone(false);
//     if (blobUrl) URL.revokeObjectURL(blobUrl);
//     setBlobUrl(null);
//     if (inputRef.current) inputRef.current.value = "";
//   };

//   const process = async () => {
//     if (files.length === 0) { toast.error("Please choose a folder first"); return; }
//     setProcessing(true);
//     // Simulated parsing delay
//     await new Promise(r => setTimeout(r, 1200));

//     // Build a mock reconciled report
//     const now = new Date();
//     const summary = [
//       ["Reconova — Parsed Report"],
//       ["Parser", name],
//       ["User", session?.email || ""],
//       ["Folder", folderName],
//       ["Files processed", files.length],
//       ["Generated at", now.toLocaleString("en-IN")],
//     ];
//     const filesSheet = [
//       ["#", "File name", "Path", "Size (KB)"],
//       ...files.map((f, i) => [i + 1, f.name, f.path, (f.size / 1024).toFixed(2)]),
//     ];
//     const rows: (string | number)[][] = [
//       ["Order ID", "Date", "Customer", "Gross (₹)", "Commission (₹)", "Tax (₹)", "Payout (₹)", "Status"],
//     ];
//     for (let i = 0; i < Math.max(20, files.length * 3); i++) {
//       const gross = Math.floor(200 + Math.random() * 2800);
//       const commission = Math.floor(gross * 0.18);
//       const tax = Math.floor(gross * 0.05);
//       const payout = gross - commission - tax;
//       const d = new Date(now.getTime() - Math.floor(Math.random() * 30) * 86400000);
//       rows.push([
//         `${name.slice(0, 3).toUpperCase()}-${100000 + i}`,
//         d.toLocaleDateString("en-IN"),
//         ["Aarav", "Priya", "Rohan", "Neha", "Kabir", "Isha"][i % 6],
//         gross, commission, tax, payout,
//         Math.random() > 0.1 ? "Settled" : "Pending",
//       ]);
//     }

//     const wb = XLSX.utils.book_new();
//     XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(summary), "Summary");
//     XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows), "Reconciliation");
//     XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(filesSheet), "Files");

//     const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
//     const blob = new Blob([wbout], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
//     const url = URL.createObjectURL(blob);
//     setBlobUrl(url);

//     if (session) logActivity(session.id, session.email, name);
//     setProcessing(false);
//     setDone(true);
//     toast.success("Report generated. Ready to download.");

//     // Auto-trigger download
//     const a = document.createElement("a");
//     a.href = url;
//     a.download = `${name}_report_${now.toISOString().slice(0, 10)}.xlsx`;
//     document.body.appendChild(a); a.click(); a.remove();
//   };

//   if (!session) return null;

//   if (!isValid) {
//     return (
//       <div className="min-h-screen bg-background">
//         <Navbar />
//         <main className="mx-auto max-w-3xl px-6 py-20 text-center">
//           <h1 className="text-2xl font-bold">Unknown parser</h1>
//           <p className="mt-2 text-muted-foreground">"{name}" is not available.</p>
//           <Link to="/dashboard"><Button className="mt-6">Back to dashboard</Button></Link>
//         </main>
//         <Footer />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-background">
//       <Navbar />
//       <main className="mx-auto max-w-4xl px-6 py-10">
//         <Link to="/dashboard" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary">
//           <ArrowLeft className="h-4 w-4" /> Back to dashboard
//         </Link>

//         <div className="mt-4 rounded-2xl border border-border bg-gradient-hero p-8">
//           <div className="flex items-center gap-4">
//             <div className="grid h-14 w-14 place-items-center rounded-xl bg-gradient-brand text-2xl font-bold text-white">{name[0]}</div>
//             <div>
//               <h1 className="text-3xl font-bold">{name} Parser</h1>
//               <p className="text-muted-foreground">Upload your {name} data folder to reconcile and export as Excel.</p>
//             </div>
//           </div>
//         </div>

//         {/* Steps */}
//         <div className="mt-8 grid gap-4 md:grid-cols-3">
//           <StepCard n={1} title="Choose folder" desc="Select the folder that contains your raw files." />
//           <StepCard n={2} title="Process" desc="We parse & reconcile the data securely in your browser." />
//           <StepCard n={3} title="Download Excel" desc="Get a ready-to-use .xlsx report instantly." />
//         </div>

//         {/* Uploader */}
//         <div className="mt-8 rounded-2xl border border-border bg-card p-8 shadow-sm">
//           <input
//             ref={inputRef}
//             type="file"
//             multiple
//             hidden
//             onChange={onPick}
//             // @ts-expect-error non-standard folder-select attrs
//             webkitdirectory="true"
//             directory="true"
//           />

//           {files.length === 0 ? (
//             <button
//               type="button"
//               onClick={() => inputRef.current?.click()}
//               className="flex w-full flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-border bg-secondary/30 py-16 transition hover:border-primary hover:bg-accent"
//             >
//               <FolderOpen className="h-10 w-10 text-primary" />
//               <div className="text-lg font-semibold">Choose folder</div>
//               <div className="text-sm text-muted-foreground">Click to pick a folder from your computer</div>
//             </button>
//           ) : (
//             <div>
//               <div className="flex items-start justify-between gap-4">
//                 <div className="flex items-center gap-3">
//                   <FolderOpen className="h-6 w-6 text-primary" />
//                   <div>
//                     <div className="font-semibold">{folderName}</div>
//                     <div className="text-xs text-muted-foreground">{files.length} file{files.length > 1 ? "s" : ""} selected</div>
//                   </div>
//                 </div>
//                 <Button variant="ghost" size="sm" onClick={reset}><X className="mr-1 h-4 w-4" />Clear</Button>
//               </div>

//               <div className="mt-4 max-h-56 overflow-auto rounded-lg border border-border">
//                 <table className="w-full text-sm">
//                   <thead className="bg-secondary/50 text-left text-xs uppercase text-muted-foreground">
//                     <tr><th className="px-4 py-2">File</th><th className="px-4 py-2">Path</th><th className="px-4 py-2 text-right">Size</th></tr>
//                   </thead>
//                   <tbody>
//                     {files.slice(0, 200).map((f, i) => (
//                       <tr key={i} className="border-t border-border">
//                         <td className="px-4 py-2 font-medium">{f.name}</td>
//                         <td className="px-4 py-2 text-muted-foreground">{f.path}</td>
//                         <td className="px-4 py-2 text-right text-muted-foreground">{(f.size / 1024).toFixed(1)} KB</td>
//                       </tr>
//                     ))}
//                   </tbody>
//                 </table>
//                 {files.length > 200 && <div className="border-t border-border p-2 text-center text-xs text-muted-foreground">+ {files.length - 200} more…</div>}
//               </div>

//               <div className="mt-6 flex flex-wrap gap-3">
//                 <Button onClick={process} disabled={processing} className="bg-gradient-brand text-white">
//                   {processing ? <><Loader2 className="mr-1 h-4 w-4 animate-spin" /> Processing…</> : <><FileSpreadsheet className="mr-1 h-4 w-4" /> Process & get Excel</>}
//                 </Button>
//                 {done && blobUrl && (
//                   <a href={blobUrl} download={`${name}_report.xlsx`}>
//                     <Button variant="outline"><Download className="mr-1 h-4 w-4" /> Download again</Button>
//                   </a>
//                 )}
//                 {done && (
//                   <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
//                     <CheckCircle2 className="h-3.5 w-3.5" /> Report ready
//                   </span>
//                 )}
//               </div>
//             </div>
//           )}

//           <p className="mt-4 text-xs text-muted-foreground">
//             Your files never leave your browser in this preview. When connected to your FastAPI backend, they'll be uploaded securely to your server.
//           </p>
//         </div>
//       </main>
//       <Footer />
//       <CookieNotice />
//     </div>
//   );
// }

// function StepCard({ n, title, desc }: { n: number; title: string; desc: string }) {
//   return (
//     <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
//       <div className="grid h-7 w-7 place-items-center rounded-full bg-primary text-xs font-bold text-primary-foreground">{n}</div>
//       <div className="mt-2 font-semibold">{title}</div>
//       <div className="text-xs text-muted-foreground">{desc}</div>
//     </div>
//   );
// }

import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api"; // Aapka Axios instance config
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CookieNotice } from "@/components/CookieNotice";
import { Button } from "@/components/ui/button";
import { getSession } from "@/lib/auth";
import { logActivity, PARSERS } from "@/lib/activity";
import { toast } from "sonner";
import { ArrowLeft, FolderOpen, FileSpreadsheet, Loader2, CheckCircle2, X, Download } from "lucide-react";

export const Route = createFileRoute("/parser/$name")({
  component: ParserPage,
  head: ({ params }) => ({
    meta: [{ title: `${params.name} Parser — Reconova` }],
  }),
});

interface PickedFile { name: string; path: string; size: number; file: File; }

function ParserPage() {
  const { name } = Route.useParams();
  const nav = useNavigate();
  const inputRef = useRef<HTMLInputElement | null>(null);
  
  const [session, setSession] = useState<ReturnType<typeof getSession>>(null);
  const [files, setFiles] = useState<PickedFile[]>([]);
  const [folderName, setFolderName] = useState<string>("");
  const [blobUrl, setBlobUrl] = useState<string | null>(null);

  const isValid = PARSERS.includes(name as (typeof PARSERS)[number]);

  useEffect(() => {
    const s = getSession();
    if (!s) { nav({ to: "/login" }); return; }
    setSession(s);
  }, [nav]);

  const onPick = (e: React.ChangeEvent<HTMLInputElement>) => {
    const list = e.target.files;
    if (!list || list.length === 0) return;
    const arr: PickedFile[] = [];
    let root = "";
    for (let i = 0; i < list.length; i++) {
      const f = list[i];
      const rel: string = (f as File & { webkitRelativePath?: string }).webkitRelativePath || f.name;
      if (!root && rel.includes("/")) root = rel.split("/")[0];
      arr.push({ name: f.name, path: rel, size: f.size, file: f });
    }
    setFolderName(root || "Selected files");
    setFiles(arr);
    if (blobUrl) { URL.revokeObjectURL(blobUrl); setBlobUrl(null); }
  };

  const reset = () => {
    setFiles([]); setFolderName("");
    if (blobUrl) URL.revokeObjectURL(blobUrl);
    setBlobUrl(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  // 🚀 Actual FastAPI Backend Integration using TanStack Query Mutation
  const {  mutate: startBackendParsing, isPending: processing, isSuccess: done } = useMutation({
    mutationFn: async () => {
      if (files.length === 0) throw new Error("Please choose a folder first");

      const formData = new FormData();
      // Har single file ko array iterator se nikal kar form data mein append kiya
      files.forEach((f) => {
        formData.append("files", f.file);
      });

      // FastAPI Endpoint hit hoga: /parsers/{name}/upload
      // Hame dynamic arraybuffer binary data return milega backend se (responseType blob)
      // const response = await api.post(`/parsers/${name}/upload`, formData, {
      //   headers: {
      //     "Content-Type": "multipart/form-data",
      //   },
      //   responseType: "blob",
      // });
      const response = await api.post(`/${name.toLowerCase()}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        responseType: "blob",
      });

      return response.data;
    },
    onSuccess: (blobData) => {
      const now = new Date();
      // Backend file binary content se real client download URL generate kiya
      const url = URL.createObjectURL(new Blob([blobData], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" }));
      setBlobUrl(url);

      if (session) logActivity(session.id, session.email, name);
      toast.success("Backend processed! Report generated successfully.");

      // Automatic Trigger download down to local machine
      const a = document.createElement("a");
      a.href = url;
      a.download = `${name}_report_${now.toISOString().slice(0, 10)}.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    },
    onError: (error: any) => {
      console.error("Backend Error: ", error);
      toast.error(error?.response?.data?.detail || "Failed to process files on backend server.");
    }
  });

  if (!session) return null;

  if (!isValid) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="mx-auto max-w-3xl px-6 py-20 text-center">
          <h1 className="text-2xl font-bold">Unknown parser</h1>
          <p className="mt-2 text-muted-foreground">"{name}" is not available.</p>
          <Link to="/dashboard"><Button className="mt-6">Back to dashboard</Button></Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main className="mx-auto max-w-4xl px-6 py-10">
        <Link to="/dashboard" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary">
          <ArrowLeft className="h-4 w-4" /> Back to dashboard
        </Link>

        <div className="mt-4 rounded-2xl border border-border bg-gradient-hero p-8">
          <div className="flex items-center gap-4">
            <div className="grid h-14 w-14 place-items-center rounded-xl bg-gradient-brand text-2xl font-bold text-white">{name[0]}</div>
            <div>
              <h1 className="text-3xl font-bold">{name} Parser</h1>
              <p className="text-muted-foreground">Upload your {name} data folder to reconcile and export as Excel.</p>
            </div>
          </div>
        </div>

        {/* Steps */}
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <StepCard n={1} title="Choose folder" desc="Select the folder that contains your raw files." />
          <StepCard n={2} title="Process" desc="We parse & reconcile the data securely via FastAPI backend." />
          <StepCard n={3} title="Download Excel" desc="Get a ready-to-use .xlsx report instantly." />
        </div>

        {/* Uploader */}
        <div className="mt-8 rounded-2xl border border-border bg-card p-8 shadow-sm">
          <input
            ref={inputRef}
            type="file"
            multiple
            hidden
            onChange={onPick}
            // @ts-expect-error non-standard folder-select attrs
            webkitdirectory="true"
            directory="true"
          />

          {files.length === 0 ? (
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="flex w-full flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed border-border bg-secondary/30 py-16 transition hover:border-primary hover:bg-accent"
            >
              <FolderOpen className="h-10 w-10 text-primary" />
              <div className="text-lg font-semibold">Choose folder</div>
              <div className="text-sm text-muted-foreground">Click to pick a folder from your computer</div>
            </button>
          ) : (
            <div>
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <FolderOpen className="h-6 w-6 text-primary" />
                  <div>
                    <div className="font-semibold">{folderName}</div>
                    <div className="text-xs text-muted-foreground">{files.length} file{files.length > 1 ? "s" : ""} selected</div>
                  </div>
                </div>
                <Button variant="ghost" size="sm" onClick={reset} disabled={processing}><X className="mr-1 h-4 w-4" />Clear</Button>
              </div>

              <div className="mt-4 max-h-56 overflow-auto rounded-lg border border-border">
                <table className="w-full text-sm">
                  <thead className="bg-secondary/50 text-left text-xs uppercase text-muted-foreground">
                    <tr><th className="px-4 py-2">File</th><th className="px-4 py-2">Path</th><th className="px-4 py-2 text-right">Size</th></tr>
                  </thead>
                  <tbody>
                    {files.slice(0, 200).map((f, i) => (
                      <tr key={i} className="border-t border-border">
                        <td className="px-4 py-2 font-medium">{f.name}</td>
                        <td className="px-4 py-2 text-muted-foreground">{f.path}</td>
                        <td className="px-4 py-2 text-right text-muted-foreground">{(f.size / 1024).toFixed(1)} KB</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {files.length > 200 && <div className="border-t border-border p-2 text-center text-xs text-muted-foreground">+ {files.length - 200} more…</div>}
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <Button onClick={() => startBackendParsing()} disabled={processing} className="bg-gradient-brand text-white">
                  {processing ? <><Loader2 className="mr-1 h-4 w-4 animate-spin" /> Uploading & Processing…</> : <><FileSpreadsheet className="mr-1 h-4 w-4" /> Upload & Reconcile (FastAPI)</>}
                </Button>
                {done && blobUrl && (
                  <a href={blobUrl} download={`${name}_report.xlsx`}>
                    <Button variant="outline"><Download className="mr-1 h-4 w-4" /> Download again</Button>
                  </a>
                )}
                {done && (
                  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
                    <CheckCircle2 className="h-3.5 w-3.5" /> Report ready
                  </span>
                )}
              </div>
            </div>
          )}

          <p className="mt-4 text-xs text-muted-foreground">
            Connected to production FastAPI backend securely. Files will be parsed and transformed directly on the server database.
          </p>
        </div>
      </main>
      <Footer />
      <CookieNotice />
    </div>
  );
}

function StepCard({ n, title, desc }: { n: number; title: string; desc: string }) {
  return (
    <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
      <div className="grid h-7 w-7 place-items-center rounded-full bg-primary text-xs font-bold text-primary-foreground">{n}</div>
      <div className="mt-2 font-semibold">{title}</div>
      <div className="text-xs text-muted-foreground">{desc}</div>
    </div>
  );
}
