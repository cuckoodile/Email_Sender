import { useQuery } from "@tanstack/react-query";
import { BASE_URL } from "../api-config";

export const useGetUsers = (userType = null) => {
  return useQuery({
    queryKey: ['users', userType],
    queryFn: async () => {
      let url = `${BASE_URL}/members/`;
      if (userType) {
        url += `?type=${userType}`;
      }

      const token = localStorage.getItem('token');
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Clear auth data if unauthorized
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login'; // Redirect to login
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch users");
      }

      return response.json();
    },
    enabled: !!localStorage.getItem('token')
  });
};