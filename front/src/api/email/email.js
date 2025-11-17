import { useMutation, useQuery } from "@tanstack/react-query";
import { BASE_URL } from "../api-config";

export const usePostEmail = () => {
  return useMutation({
    mutationFn: async (emailData) => {
      let formData;

      if (emailData instanceof FormData) {
        // If emailData is already FormData (with file attachment), use it directly
        formData = emailData;
      } else {
        // If emailData is a regular object, create FormData from it
        formData = new FormData();

        // Create a copy of the emailData to avoid potential issues
        const emailDataCopy = { ...emailData };

        // Add the email data as appropriate
        Object.keys(emailDataCopy).forEach(key => {
          const value = emailDataCopy[key];
          if (Array.isArray(value)) {
            // For recipient lists, stringify the array
            formData.append(key, JSON.stringify(value));
          } else {
            formData.append(key, value);
          }
        });
      }

      const token = localStorage.getItem('token');
      const response = await fetch(`${BASE_URL}/email-burst/`, {
        method: "POST",
        headers: {
          // Note: Don't set Content-Type header when using FormData (browser sets it with boundary)
          "Authorization": `Bearer ${token}`
        },
        body: formData,
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Clear auth data if unauthorized
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login'; // Redirect to login
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to send email");
      }

      return response.json();
    },
  });
};

export const useGetEmailBursts = () => {
  return useQuery({
    queryKey: ['email-bursts'],
    queryFn: async () => {
      const token = localStorage.getItem('token');
      const response = await fetch(`${BASE_URL}/email-burst/`, {
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
        throw new Error(errorData.detail || "Failed to fetch email bursts");
      }

      return response.json();
    },
    enabled: !!localStorage.getItem('token')
  });
};

export const useGetEmailBurstByUser = (userId) => {
  return useQuery({
    queryKey: ['email-bursts-by-user', userId],
    queryFn: async () => {
      const token = localStorage.getItem('token');
// NOTE: Backend doesn't have a user-specific email burst endpoint, so we'll fetch all and filter client-side
      const response = await fetch(`${BASE_URL}/email-burst/`, {
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
        throw new Error(errorData.detail || "Failed to fetch user's email bursts");
      }

      const data = await response.json();
      // Filter results by userId if provided (backend may not have this endpoint)
      if (data && data.results) {
        // Assuming the data has a user_id field to filter by
        const filteredResults = data.results.filter(item => item.user_id === userId || item.created_by === userId);
        return { ...data, results: filteredResults };
      } else if (Array.isArray(data)) {
        // If it's a simple array
        return data.filter(item => item.user_id === userId || item.created_by === userId);
      }
      return data;
    },
    enabled: !!localStorage.getItem('token') && !!userId
  });
};