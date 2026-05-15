function SummaryPanel({ items }) {

  const summary = {
    total: items.length,
    draft: items.filter(i => i.state === "draft").length,
    active: items.filter(i => i.state === "active").length,
    blocked: items.filter(i => i.state === "blocked").length,
    completed: items.filter(i => i.state === "completed").length
  };

  return (
    <div className="summary-panel">
      <div>Total: {summary.total}</div>
      <div>Draft: {summary.draft}</div>
      <div>Active: {summary.active}</div>
      <div>Blocked: {summary.blocked}</div>
      <div>Completed: {summary.completed}</div>
    </div>
  );
}

export default SummaryPanel;