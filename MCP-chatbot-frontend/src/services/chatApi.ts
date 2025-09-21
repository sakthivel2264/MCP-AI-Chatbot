export interface ChatMessage {
  message: string;
}

export interface ChatResponse {
  // Add the expected response structure here based on your API
  // For now, assuming it returns a message field
  message?: string;
  response?: string;
  answer?: string;
  [key: string]: unknown | string;
}

export class ChatApiError extends Error {
  public status?: number;
  
  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ChatApiError';
    this.status = status;
  }
}

export const sendMessage = async (message: string): Promise<string> => {
  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      mode: 'cors',
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new ChatApiError(
        `HTTP error! status: ${response.status}`,
        response.status
      );
    }

    const data: ChatResponse = await response.json();
    
    // Handle different possible response formats
    return data.message || data.response || data.answer || '';
  } catch (error) {
    if (error instanceof ChatApiError) {
      throw error;
    }
    
    // Handle network errors or other issues
    throw new ChatApiError(
      error instanceof Error ? error.message : 'Failed to send message'
    );
  }
};