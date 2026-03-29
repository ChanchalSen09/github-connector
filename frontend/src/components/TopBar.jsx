import { FiBell, FiChevronDown, FiSearch } from "react-icons/fi";

export function TopBar() {
  return (
    <header className="flex h-[54px] items-center justify-between border-b border-white/5 bg-[#241a56] px-4 text-white">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2.5 text-[16px] font-semibold">
          <div className="relative flex h-7 w-7 items-center justify-center rounded-full bg-[#4f46e5] shadow-[0_6px_18px_rgba(79,70,229,0.35)]">
            <div className="h-2.5 w-2.5 rounded-full border-2 border-white" />
          </div>
          <span>Workspace</span>
        </div>
        <div className="flex items-center gap-1 rounded-lg bg-[#342a73] px-3 py-1.5 text-[11px] text-[#d4d1fb]">
          <span>Workspace 1</span>
          <FiChevronDown className="text-[10px]" />
        </div>
      </div>

      <div className="flex w-full max-w-[470px] items-center rounded-xl border border-white/10 bg-[#342a73] px-4 py-2.5 text-[13px] text-[#a6a1d8] shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
        <FiSearch className="mr-2 text-[14px]" />
        <span className="flex-1">Search...</span>
        <span className="text-[9px] tracking-[0.2em]">⌘K</span>
      </div>

      <div className="flex items-center gap-4">
        <button type="button" className="text-[#dcd9ff]">
          <FiBell className="h-[18px] w-[18px]" />
        </button>
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#4b3fb8] text-[11px] font-semibold">
          GK
        </div>
      </div>
    </header>
  );
}
