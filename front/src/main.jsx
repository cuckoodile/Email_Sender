import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import Page from "./app/dashboard/page.jsx";
import LoginPage from "./app/login/page.jsx";
import RegisterPage from "./app/register/page.jsx";
import EmailsPage from "./app/emails/page.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import { AuthProvider } from "./contexts/AuthContext.jsx";
import { queryClient } from "./lib/queryClient.js";


const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <AuthProvider>
        <App />
      </AuthProvider>
    ),
    children: [
      {
        index: true,
        path: "",
        element: (
          <ProtectedRoute>
            <Page />
          </ProtectedRoute>
        ),
      },
      {
        path: "dashboard",
        element: (
          <ProtectedRoute>
            <Page />
          </ProtectedRoute>
        ),
      },
      {
        path: "emails",
        element: (
          <ProtectedRoute>
            <EmailsPage />
          </ProtectedRoute>
        ),
      }
    ],
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/register",
    element: <RegisterPage />,
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>
);
