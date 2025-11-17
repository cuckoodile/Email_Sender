import { useMutation } from "@tanstack/react-query";
import { BASE_URL } from "../api-config";

export const useLogin = () => {
  return useMutation({
    mutationFn: async ({ username, password }) => {
      console.log("Login data: ", username, password)

      const response = await fetch(`${BASE_URL}/auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      console.log("Login response data:", data); // Debug log
      return data;
    },
  });
};