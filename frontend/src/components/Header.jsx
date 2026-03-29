import { FiSearch } from "react-icons/fi";

export function Header({ onCreateNew, searchValue, onSearchChange }) {
  return (
    <div className="flex items-center justify-between border-b border-[#eef1f6] px-6 py-5">
      <h1 className="text-[18px] font-semibold text-[#202532]">Knowledge Base</h1>

      <div className="flex items-center gap-2.5">
        <div className="flex h-12 w-[220px] items-center gap-2 rounded-xl border border-[#e4e8f0] bg-white px-4 text-[13px] text-[#8f8f9b] shadow-[0_1px_2px_rgba(15,23,42,0.04)]">
          <FiSearch className="text-[14px]" />
          <input
            value={searchValue}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search..."
            className="w-full border-0 bg-transparent p-0 text-[13px] text-[#4a4a56] outline-none placeholder:text-[#b3b3bf]"
          />
        </div>
        <button
          type="button"
          onClick={onCreateNew}
          className="flex h-12 items-center gap-2 rounded-xl bg-[#5b4ef7] px-5 text-[13px] font-semibold text-white shadow-[0_14px_30px_rgba(91,78,247,0.28)]"
        >
          <span className="text-sm leading-none">+</span>
          <span>Create New</span>
        </button>
      </div>
    </div>
  );
}
