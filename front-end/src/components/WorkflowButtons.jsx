import { workflowAction } from "../api/itemsApi";

function WorkflowButtons({ item, refresh }) {

  async function handleAction(action) {
    await workflowAction(item.id, action);

    refresh();
  }

  return (
    <div className="workflow-buttons">
      <button onClick={() => handleAction("activate")}>
        Activate
      </button>

      <button onClick={() => handleAction("block")}>
        Block
      </button>

      <button onClick={() => handleAction("complete")}>
        Complete
      </button>

      <button onClick={() => handleAction("reopen")}>
        Reopen
      </button>
    </div>
  );
}

export default WorkflowButtons;