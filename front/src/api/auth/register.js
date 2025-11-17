import { useMutation } from "@tanstack/react-query";
import { BASE_URL } from "../api-config";

export const useRegister = () => {
  return useMutation({
    mutationFn: async (userData) => {
      const response = await fetch(`${BASE_URL}/auth/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Registration failed");
      }

      return response.json();
    },
  });
};