import {
  FiActivity,
  FiBook,
  FiBox,
  FiCpu,
  FiDatabase,
  FiFolder,
  FiGrid,
  FiKey,
  FiLayers,
  FiMonitor,
  FiPlayCircle,
  FiShield,
  FiUpload,
  FiUsers,
  FiZap,
} from "react-icons/fi";
import { sections } from "../data/knowledgeBase";

function NavIcon({ type, active = false }) {
  const className = active ? "h-4 w-4 text-[#5b4ef7]" : "h-4 w-4 text-[#6b6b78]";

  switch (type) {
    case "folder":
      return <FiFolder className={className} />;
    case "cpu":
      return <FiCpu className={className} />;
    case "library":
      return <FiBook className={className} />;
    case "publish":
      return <FiUpload className={className} />;
    case "machine":
      return <FiMonitor className={className} />;
    case "queue":
      return <FiLayers className={className} />;
    case "trigger":
      return <FiZap className={className} />;
    case "job":
      return <FiBox className={className} />;
    case "execution":
      return <FiPlayCircle className={className} />;
    case "vault":
      return <FiShield className={className} />;
    case "knowledge":
      return <FiDatabase className={className} />;
    case "keystore":
      return <FiKey className={className} />;
    case "tenant":
      return <FiGrid className={className} />;
    case "integration":
      return <FiActivity className={className} />;
    case "org":
      return <FiUsers className={className} />;
    default:
      return <div className="h-4 w-4" />;
  }
}

export function Sidebar() {
  return (
    <aside className="h-full w-[214px] shrink-0 overflow-y-auto border-r border-[#e6e8f0] bg-[#f9faff] px-3 py-6 text-[13px] text-[#676b78]">
      {sections.map((section) => (
        <div key={section.title} className="mb-7 last:mb-0">
          <p className="mb-3 px-2 text-[11px] font-medium uppercase tracking-[0.04em] text-[#9ca3b5]">
            {section.title}
          </p>
          <div className="space-y-1">
            {section.items.map((item) => (
              <div
                key={item.label}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 transition ${
                  item.active
                    ? "bg-[#ece8ff] font-medium text-[#5648f3] shadow-[inset_0_1px_0_rgba(255,255,255,0.55)]"
                    : "text-[#5f6472] hover:bg-[#f2f4fa]"
                }`}
              >
                <NavIcon type={item.icon} active={item.active} />
                <span className="truncate">{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </aside>
  );
}

