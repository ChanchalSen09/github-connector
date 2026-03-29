export const sections = [
  {
    title: "MY PROJECTS",
    items: [
      { label: "Agents", icon: "folder" },
      { label: "AI Models", icon: "cpu" },
      { label: "Library", icon: "library" },
    ],
  },
  {
    title: "ORCHESTRATOR",
    items: [
      { label: "Published", icon: "publish" },
      { label: "Machines", icon: "machine" },
      { label: "Queues", icon: "queue" },
      { label: "Triggers", icon: "trigger" },
      { label: "Jobs", icon: "job" },
      { label: "Executions", icon: "execution" },
      { label: "Vault", icon: "vault" },
      { label: "Knowledge Base", icon: "knowledge", active: true },
      { label: "Key Store", icon: "keystore" },
    ],
  },
  {
    title: "ADMIN",
    items: [
      { label: "Tenant", icon: "tenant" },
      { label: "Integrations", icon: "integration" },
      { label: "Organization", icon: "org" },
    ],
  },
];

export const knowledgeCards = Array.from({ length: 6 }, () => ({
  title: "Test",
  description:
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy",
  createdOn: "14/07/2025",
}));
