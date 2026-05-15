import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createItem } from "../api/itemsApi";

function CreateItemPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: 0
  });

  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;

    setForm({
      ...form,
      [name]: name === "priority"
        ? Number(value)
        : value
    });
  }

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const response = await createItem(form);

      console.log(response.data);

      navigate(`/items/${response.data.data.id}`);
    } catch (err) {
      console.log(err.response?.data);

      setError(
        err.response?.data?.error ||
        "Failed to create item"
      );
    }
  }

  return (
    <div className="card">
      <h2>Create Item</h2>

      {error && <p>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="title"
          value={form.title}
          placeholder="Title"
          onChange={handleChange}
          required
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
          onChange={handleChange}
        />

        <button type="submit">
          Create
        </button>
      </form>
    </div>
  );
}

export default CreateItemPage;