'use server';

import { generateId } from 'ai';
import { createAI, createStreamableUI, createStreamableValue } from 'ai/rsc';
import { OpenAI } from 'openai';
import { ReactNode } from 'react';
import { Message } from './message';
import { Citation } from './interfaces/citation.interface';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export interface ClientMessage {
  id: string;
  status: ReactNode;
  text: ReactNode;
}

let ASSISTANT_ID = '';
let THREAD_ID = '';
let RUN_ID = '';

/**
 * Fetch existing assistant id from the server
 * @improvement move this to a separate file
 */
async function fetchAssistantId() {
  const response = await fetch(process.env.APP_API_URL + '/assistant');
  const data = await response.json();
  return data
}

export async function submitMessage(question: string): Promise<ClientMessage> {
  const statusUIStream = createStreamableUI('thread.init');

  const textStream = createStreamableValue('');
  const textUIStream = createStreamableUI(
    <Message textStream={textStream.value} />,
  );

  const runQueue = [];

  let annotations: Citation[] = [];

  // Ensure assistant id is fetched before proceeding
  if (!ASSISTANT_ID) {
    ASSISTANT_ID = await fetchAssistantId();
  }
  
  (async () => {
  
    if (THREAD_ID) {
      await openai.beta.threads.messages.create(THREAD_ID, {
        role: 'user',
        content: question,
      });

      const run = await openai.beta.threads.runs.create(THREAD_ID, {
        assistant_id: ASSISTANT_ID,
        stream: true,
      });

      runQueue.push({ id: generateId(), run });
    } else {
      const run = await openai.beta.threads.createAndRun({
        assistant_id: ASSISTANT_ID,
        stream: true,
        thread: {
          messages: [{ role: 'user', content: question }],
        },
      });

      runQueue.push({ id: generateId(), run });
    }

    while (runQueue.length > 0) {
      const latestRun = runQueue.shift();

      if (latestRun) {
        for await (const delta of latestRun.run) {
          const { data, event } = delta;

          statusUIStream.update(event);

          if (event === 'thread.created') {
            THREAD_ID = data.id;
          } else if (event === 'thread.run.created') {
            RUN_ID = data.id;
          } else if (event === 'thread.message.delta') {
            data.delta.content?.map(async part => {
              if (part.type === 'text') {
                if (part.text) {
                  if (part.text.value && part.text.annotations) {
                    // replace value with annotation index
                    for (let index = 0; index < part.text.annotations.length; index++) {
                      const annotation = part.text.annotations[index];
                      part.text.value = part.text.value.replace(annotation.text || '', `[${index}]`);
                      annotations.push(annotation);
                    }
                  }
                  textStream.append(part.text.value as string);
                }
              }
            });
          } else if (event === 'thread.run.failed') {
            console.error(data);
          }
        }
      }
    }

    // process annotations
    textStream.append(await processMessageAnnotation(annotations));

    statusUIStream.done();
    textStream.done();
  })();

  return {
    id: generateId(),
    status: statusUIStream.value,
    text: textUIStream.value,
  };
}

async function processMessageAnnotation(annotations: Citation[]): Promise<string> {
  let citations: string[] = [];
  for (const annotation of annotations) {
    if (annotation.file_citation?.file_id) {
      const citedFile = await openai.files.retrieve(annotation.file_citation.file_id);
      citations.push(`[${annotation.index}] ${annotation.file_citation.quote} from ${citedFile.filename}`);
    }
  }
  return citations.length > 0 ? "\n" + citations.join("\n") : '';
}

export const AI = createAI({
  actions: {
    submitMessage,
  },
});