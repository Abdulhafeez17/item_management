import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getItem, updateItem } from "../api/itemsApi";

function EditItemPage() {
  const { id } = useParams();

  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: 0
  });

  useEffect(() => {
    loadItem();
  }, []);

  async function loadItem() {
    const response = await getItem(id);

    setForm(response.data);
  }

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    await updateItem(id, form);

    navigate(`/items/${id}`);
  }

  return (
    <div className="card">
      <h2>Edit Item</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="title"
          value={form.title}
          placeholder="Title"
          onChange={handleChange}
        />

        <textarea
          name="description"
          value={form.description}
          placeholder="Description"
          onChange={handleChange}
        />

        <input
          type="number"
          name="priority"
          
          value={form.priority}
          placeholder="priority"
          onChange={handleChange}
        />

        <button type="submit">
          Save
        </button>
      </form>
    </div>
  );
}

export default EditItemPage;