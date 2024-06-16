import { PaperAirplaneIcon } from '@heroicons/react/20/solid';

interface FixedInputSectionProps {
  input: string;
  setInput: (input: string) => void;
  handleSubmission: () => void;
}

export default function ChatInput({ input, setInput, handleSubmission }: FixedInputSectionProps) {
  const isInputEmpty = input.trim() === '';

  return (
    <div className="flex flex-row gap-2 p-2 bg-zinc-100 w-full">
        <div className="backdrop-blur-sm bg-white/30 fixed w-[98%] sm:w-[91%] ml-[1%] left-0 sm:ml-[-2%] sm:left-auto md:w-[91.5%] lg:w-[67.5%] xl:w-full max-w-3xl bottom-0">
            <input
              className="text-md text-gray-500 bg-gray-100 w-full rounded-2xl mb-2 sm:mb-3 shadow-xl p-2 pl-4 sm:p-3 sm:pl-5 focus:outline-none"
              placeholder="Ask a question"
              value={input}
              onChange={event => setInput(event.target.value)}
              onKeyDown={event => {
                if (event.key === 'Enter' && !isInputEmpty) {
                  handleSubmission();
                }
              }}
            />
            <button
              onClick={() => {
                if (!isInputEmpty) {
                  handleSubmission();
                }
              }}
              className={`absolute right-1 mt-1 sm:mt-[6.5px] sm:mr-[3px] rounded-xl px-2 pr-1.5 py-1.5 text-sm font-semibold text-white shadow-sm ring-0 ${isInputEmpty ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700'}`}
              disabled={isInputEmpty}
            >
              <PaperAirplaneIcon className="h-5 w-5 sm:h-6 sm:w-6 sm:ml-[2px] sm:mt-[0.25px] inline" aria-hidden="true"/>
            </button>
            <p className="text-xs text-gray-500 text-center mb-2 sm:mb-3 mr-2 sm:mr-4">
                Made by Alfonso Hernandez. Review source code on <span className="font-semibold"><a href="https://github.com/aheruz/Smart-Spreadsheet" target="_blank" className="underline">GitHub</a></span>
            </p>
        </div>
    </div>
  );
}