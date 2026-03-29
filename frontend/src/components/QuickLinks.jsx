export function QuickLinks({ links }) {
  return (
    <div className="rounded-[28px] border border-white/70 bg-white/90 p-6 shadow-panel">
      <p className="text-sm font-medium text-primary">Quick links</p>
      <h3 className="mt-1 text-xl font-semibold text-ink">Start from a structured flow</h3>
      <div className="mt-5 grid gap-3">
        {links.map((link) => (
          <div
            key={link}
            className="rounded-2xl border border-line bg-slate-50 px-4 py-3 text-sm font-medium text-slate-600"
          >
            {link}
          </div>
        ))}
      </div>
    </div>
  );
}
