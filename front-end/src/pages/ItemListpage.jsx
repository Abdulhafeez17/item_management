import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import {
  getItems,
  searchItems,
  paginateItems,
  searchPaginatedItems
} from "../api/itemsApi";

import Loading from "../components/Loading";
import EmptyState from "../components/EmptyState";
import ErrorMessage from "../components/ErrorMessage";
import SummaryPanel from "../components/SummaryPanel";

function ItemListPage() {
  const [items, setItems] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [filter, setFilter] = useState("all");

  const [search, setSearch] = useState("");

  const [page, setPage] = useState(1);

  const limit = 5;

  useEffect(() => {
    fetchItems();
  }, [page]);

  async function fetchItems() {
    try {
      setLoading(true);

      const offset = (page - 1) * limit;

      const response = await paginateItems(
        limit,
        offset
      );

      setItems(response.data.data || []);
    } catch (err) {
      console.log(err);

      setError("Failed to load items");
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch() {
    try {
      setLoading(true);

      if (search.trim() === "") {
        fetchItems();
        return;
      }

      const offset = (page - 1) * limit;

      const response =
        await searchPaginatedItems(
          search,
          limit,
          offset
        );

      setItems(response.data.data || []);
    } catch (err) {
      console.log(err);

      setError("Search failed");
    } finally {
      setLoading(false);
    }
  }

  const filteredItems =
    filter === "all"
      ? items
      : items.filter(
          (item) => item.state === filter
        );

  if (loading) return <Loading />;

  if (error)
    return <ErrorMessage message={error} />;

  return (
    <div>
      <div className="top-bar">
        <h1>Items</h1>

        {/* FILTER */}
        <select
          value={filter}
          onChange={(e) =>
            setFilter(e.target.value)
          }
        >
          <option value="all">All</option>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="blocked">Blocked</option>
          <option value="completed">
            Completed
          </option>
          <option value="archived">
            Archived
          </option>
        </select>
      </div>

      {/* SEARCH */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px"
        }}
      >
        <input
          type="text"
          placeholder="Search items..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

        <button onClick={handleSearch}>
          Search
        </button>

        <button onClick={fetchItems}>
          Reset
        </button>
      </div>

      <SummaryPanel items={items} />

      {filteredItems.length === 0 ? (
        <EmptyState message="No items found" />
      ) : (
        <>
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Priority</th>
                <th>State</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {filteredItems.map((item) => (
                <tr key={item.id}>
                  <td>{item.title}</td>

                  <td>{item.priority}</td>

                  <td>{item.state}</td>

                  <td>
                    <Link
                      to={`/items/${item.id}`}
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* PAGINATION */}
          <div
            style={{
              marginTop: "20px",
              display: "flex",
              gap: "10px"
            }}
          >
            <button
              disabled={page === 1}
              onClick={() =>
                setPage(page - 1)
              }
            >
              Previous
            </button>

            <span>Page {page}</span>

            <button
              onClick={() =>
                setPage(page + 1)
              }
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ItemListPage;