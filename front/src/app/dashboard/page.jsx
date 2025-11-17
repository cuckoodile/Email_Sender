import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import UserDataTable from "@/components/UserDataTable";
import { useGetUsers } from "@/api/user/users";
import { useGetEmailBurstByUser } from "@/api/email/email";

export default function Page() {
  const { user } = useAuth(); // Get the current logged in user
  const { data: users, isLoading: usersLoading, error: usersError } = useGetUsers(); // Fetch all users
  const { data: emailBursts, isLoading: burstsLoading, error: burstsError } = useGetEmailBurstByUser(user?.id); // Fetch email bursts by current user

  if (usersError) {
    return <div className="p-4">Error loading users: {usersError.message}</div>;
  }

  if (burstsError) {
    return <div className="p-4">Error loading email bursts: {burstsError.message}</div>;
  }

  console.log("Users: ", users);
  console.log("Email Bursts: ", emailBursts);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Users</h2>
        <UserDataTable
          data={users?.results || users || []}
          isLoading={usersLoading}
        />
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Email Burst History</h2>
        {burstsLoading ? (
          <p>Loading email bursts...</p>
        ) : emailBursts && (emailBursts.results || emailBursts.length) ? (
          <div className="border rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {(emailBursts.results || emailBursts).map((burst, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs truncate" title={burst.subject}>
                      {burst.subject}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(burst.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {burst.is_sent ? 'Sent' : 'Pending'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No email bursts found.</p>
        )}
      </div>
    </div>
  );
}
