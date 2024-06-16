'use client';

import { useState } from 'react';
import { ClientMessage } from './actions';
import { useActions } from 'ai/rsc';
import ChatInput from './components/chat.input';

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ClientMessage[]>([]);
  const { submitMessage } = useActions();

  const handleSubmission = async () => {
    setMessages(currentMessages => [
      ...currentMessages,
      {
        id: Date.now().toString(),
        status: 'user.message.created',
        text: input,
        gui: null,
      },
    ]);

    const response = await submitMessage(input);
    setMessages(currentMessages => [...currentMessages, response]);
    setInput('');
  };

  return (
    <div className="flex flex-col-reverse mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
      
      <ChatInput input={input} setInput={setInput} handleSubmission={handleSubmission} />
      <div className="flex flex-col p-0 h-[calc(100dvh-56px)]">
        <div>
          {messages.map(message => (
            <div key={message.id} className="flex flex-col gap-1 border-b p-2">
              <div className="flex flex-row justify-between">
                <div className="text-sm text-zinc-500">{message.status}</div>
              </div>
              <div>{message.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}