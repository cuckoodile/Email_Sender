import React, { useState } from 'react';
import { usePostEmail, useGetEmailBursts } from '@/api/email/email';
import { useGetUsers } from '@/api/user/users';
import { useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export default function EmailsPage() {
  const [emailData, setEmailData] = useState({
    subject: '',
    body: '',
    recipients: [],
    sendOption: 'individual', // 'all', 'selected', 'individual'
    attachment: null,
  });

  const [selectedRecipients, setSelectedRecipients] = useState([]);
  const [recipientEmail, setRecipientEmail] = useState('');

  const queryClient = useQueryClient();
  const postEmailMutation = usePostEmail();
  const { data: users, isLoading: usersLoading } = useGetUsers('non-staff');
  const { data: emailBursts, isLoading: burstsLoading, error: burstsError } = useGetEmailBursts();

  const handleInputChange = (field, value) => {
    setEmailData(prev => ({
      ...prev,
      [field]: value
    }));
  };


  const handleFileChange = (e) => {
    setEmailData(prev => ({
      ...prev,
      attachment: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      let recipientsToSend = [];

      // Determine recipients based on send option
      if (emailData.sendOption === 'individual') {
        // For individual, just use the selected recipient email
        recipientsToSend = recipientEmail ? [recipientEmail] : [];
      } else if (emailData.sendOption === 'selected') {
        recipientsToSend = [...selectedRecipients]; // Use the selected recipients
      } else if (emailData.sendOption === 'all') {
        // For 'all' option, fetch all non-staff users and get their emails
        const allUsers = users?.results ? [...users.results] : users ? [...users] : [];
        recipientsToSend = allUsers.map(user => user.email);
      }

      // Validate recipients
      if (!recipientsToSend.length) {
        alert('Please select at least one recipient');
        return;
      }

      // Prepare email data
      const emailPayload = {
        subject: emailData.subject,
        body: emailData.body,
        send_option: emailData.sendOption,
        recipients: [...recipientsToSend], // Ensure we create a new array
      };

      // If there's an attachment, we need to use FormData
      let payload;
      if (emailData.attachment) {
        payload = new FormData();
        payload.append('subject', emailData.subject);
        payload.append('body', emailData.body);
        payload.append('send_option', emailData.sendOption);
        payload.append('recipients', JSON.stringify([...recipientsToSend]));
        payload.append('attachment', emailData.attachment);
      } else {
        payload = { ...emailPayload }; // Create a new object to avoid any reference issues
      }

      await postEmailMutation.mutateAsync(payload);
      alert('Email sent successfully!');

      // Invalidate and refetch email bursts to update the UI
      await queryClient.invalidateQueries({ queryKey: ['email-bursts'] });

      // Reset form
      setEmailData({
        subject: '',
        body: '',
        recipients: [],
        sendOption: 'individual',
        attachment: null,
      });
      setSelectedRecipients([]);
      setRecipientEmail('');
    } catch (error) {
      alert(error.message || 'Failed to send email');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Email Composer</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">Compose New Email</h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <div>
                <Label htmlFor="subject">Subject</Label>
                <Input
                  id="subject"
                  value={emailData.subject}
                  onChange={(e) => handleInputChange('subject', e.target.value)}
                  required
                />
              </div>

              <div>
                <Label htmlFor="body">Email Body</Label>
                <Textarea
                  id="body"
                  value={emailData.body}
                  onChange={(e) => handleInputChange('body', e.target.value)}
                  rows={10}
                  required
                />
              </div>

              <div>
                <Label>Send To</Label>
                <Select
                  value={emailData.sendOption}
                  onValueChange={(value) => handleInputChange('sendOption', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select option" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="individual">Individual</SelectItem>
                    <SelectItem value="selected">Selected Users</SelectItem>
                    <SelectItem value="all">All Non-Staff</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {emailData.sendOption === 'individual' && (
                <div className="space-y-2">
                  <div>
                    <Select
                      value={recipientEmail}
                      onValueChange={setRecipientEmail}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select recipient" />
                      </SelectTrigger>
                      <SelectContent>
                        {users && (users.results || users).map((user) => (
                          <SelectItem key={user.id} value={user.email}>
                            {user.first_name} {user.last_name} ({user.email})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {recipientEmail && (
                    <div className="mt-2">
                      <p className="text-sm font-medium mb-1">Selected Recipient:</p>
                      <div className="bg-blue-100 text-blue-800 px-2 py-1 rounded flex items-center">
                        {recipientEmail}
                        <button
                          type="button"
                          className="ml-1 text-blue-600 hover:text-blue-800"
                          onClick={() => setRecipientEmail('')}
                        >
                          ×
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {emailData.sendOption === 'selected' && (
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">Select non-staff recipients:</p>
                  {usersLoading ? (
                    <p>Loading users...</p>
                  ) : (
                    <div className="max-h-60 overflow-y-auto border rounded p-2">
                      {users && users.results ? users.results.map((user) => (
                        <div key={user.id} className="flex items-center p-2 hover:bg-gray-100">
                          <input
                            type="checkbox"
                            id={`user-${user.id}`}
                            checked={selectedRecipients.includes(user.email)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedRecipients(prev => [...prev, user.email]);
                              } else {
                                setSelectedRecipients(prev => prev.filter(email => email !== user.email));
                              }
                            }}
                          />
                          <Label htmlFor={`user-${user.id}`} className="ml-2">
                            {user.first_name} {user.last_name} ({user.email})
                          </Label>
                        </div>
                      )) : users?.map((user) => (
                        <div key={user.id} className="flex items-center p-2 hover:bg-gray-100">
                          <input
                            type="checkbox"
                            id={`user-${user.id}`}
                            checked={selectedRecipients.includes(user.email)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedRecipients(prev => [...prev, user.email]);
                              } else {
                                setSelectedRecipients(prev => prev.filter(email => email !== user.email));
                              }
                            }}
                          />
                          <Label htmlFor={`user-${user.id}`} className="ml-2">
                            {user.first_name} {user.last_name} ({user.email})
                          </Label>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              <div>
                <Label htmlFor="attachment">Attachment (Optional)</Label>
                <Input
                  id="attachment"
                  type="file"
                  onChange={handleFileChange}
                />
              </div>
            </div>

            <Button type="submit" disabled={postEmailMutation.isPending}>
              {postEmailMutation.isPending ? 'Sending...' : 'Send Email'}
            </Button>
          </form>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">Email Burst History</h2>
          {burstsLoading ? (
            <p>Loading email history...</p>
          ) : burstsError ? (
            <p className="text-red-500">Error loading email history: {burstsError.message}</p>
          ) : emailBursts && emailBursts.results ? (
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
                  {emailBursts.results.map((burst, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs truncate" title={burst.subject}>
                        {burst.subject}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(burst.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {burst.status || 'Sent'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : emailBursts ? (
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
                  {emailBursts.map((burst, index) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 max-w-xs truncate" title={burst.subject}>
                        {burst.subject}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(burst.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {burst.status || 'Sent'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No email history available.</p>
          )}
        </div>
      </div>
    </div>
  );
}