import { useMutation } from "@tanstack/react-query";
import { BASE_URL } from "../api-config";

export const useVerifyToken = () => {
  return useMutation({
    mutationFn: async (token) => {
      const response = await fetch(`${BASE_URL}/token/verify/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Token verification failed");
      }
      
      return response.json();
    },
  });
};

// Simple function to verify token without using TanStack Query
export const verifyToken = async (token) => {
  try {
    const response = await fetch(`${BASE_URL}/token/verify/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });
    
    if (!response.ok) {
      return false;
    }
    
    await response.json(); // Process the response to confirm it's valid
    return true;
  } catch (error) {
    console.error("Token verification error:", error);
    return false;
  }
};