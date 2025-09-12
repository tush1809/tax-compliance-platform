const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

export const calculateTax = async (data) => {
  try {
    const response = await fetch(`${API_URL}/api/calculate-tax`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (err) {
    console.error("Error calculating tax:", err);
    return { error: err.message };
  }
};

