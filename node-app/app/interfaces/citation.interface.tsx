export interface Citation {
    index: number;
    type: string;
    text?: string;
    start_index?: number;
    end_index?: number;
    file_citation?: {
      file_id?: string;
      quote?: string;
    };
  };