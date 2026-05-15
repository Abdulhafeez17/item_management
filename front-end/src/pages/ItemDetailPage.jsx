import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";

import { getItem, deleteItem } from "../api/itemsApi";

import WorkflowButtons from "../components/WorkflowButtons";

function ItemDetailPage() {
  const { id } = useParams();

  const navigate = useNavigate();

  const [item, setItem] = useState(null);

  useEffect(() => {
    loadItem();
  }, []);

  async function loadItem() {
    try {
      const response = await getItem(id);
      setItem(response.data.data);
    } catch (error) {
      console.error(error);
    }
  }

  async function handleDelete() {
    try {
      await deleteItem(id);

      alert("Item deleted successfully");

      navigate("/");
    } catch (error) {
      console.error(error);
      alert("Delete failed");
    }
  }

  if (!item) return <p>Loading...</p>;

  return (
    <div className="card">
      <p>
        <strong>Title:</strong> {item.title}
      </p>

      <p>
        <strong>Description:</strong> {item.description}
      </p>

      <p>
        <strong>Priority:</strong> {item.priority}
      </p>

      <p>
        <strong>State:</strong> {item.state}
      </p>

      <p>
        <strong>Created:</strong> {item.created_at}
      </p>

      <p>
        <strong>Updated At:</strong> {item.updated_at}
      </p>

      {/* Edit Button */}
      <Link to={`/edit/${item.id}`}>
        <button>Edit Item</button>
      </Link>

      {/* Delete Button */}
      <button onClick={handleDelete}>
        Delete Item
      </button>

      {/* Workflow Actions */}
      <WorkflowButtons item={item} refresh={loadItem} />
    </div>
  );
}

export default ItemDetailPage;